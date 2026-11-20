/**
 * Gracie Barra São Mateus — Aplicação Principal (Vanilla JS)
 * 
 * Funcionalidades:
 * - Menu mobile acessível (abertura, fechamento por clique externo, tecla Escape e links)
 * - Filtro dinâmico da grade de horários (Todos, Gi, No-Gi)
 * - Data-binding declarativo via atributos [data-bind] a partir de window.SITE
 * - Atualização automática de ano corrente nos direitos autorais [data-year]
 * - Smooth scroll com compensação de altura do header fixo/sticky
 */

(function () {
  'use strict';

  var GBApp = {
    initialized: false,
    currentFilter: 'todos',
    isMenuOpen: false,

    /**
     * Inicializa todos os módulos da aplicação
     */
    init: function () {
      if (this.initialized) return;
      this.initialized = true;

      this.initDataBinding();
      this.initMobileMenu();
      this.initScheduleFilter();
      this.initSmoothScroll();
      this.initCurrentYear();
    },

    /**
     * Data-binding declarativo via [data-bind]
     * Lê valores de window.SITE e preenche atributos href, textContent e src
     */
    initDataBinding: function () {
      var site = window.SITE;
      if (!site) return;

      var elements = document.querySelectorAll('[data-bind]');
      elements.forEach(function (el) {
        var bindKey = el.getAttribute('data-bind');
        if (!bindKey) return;

        // Suporte a atalhos comuns
        switch (bindKey) {
          case 'wa':
          case 'whatsapp':
            if (el.tagName === 'A') {
              el.setAttribute('href', site.contact.whatsappUrl);
            }
            if (el.getAttribute('data-bind-text') !== null || el.textContent.trim() === '') {
              el.textContent = site.contact.phone;
            }
            break;

          case 'phone':
            if (el.tagName === 'A') {
              el.setAttribute('href', 'tel:+55' + (site.contact.phoneRaw || '27999494456'));
            }
            el.textContent = site.contact.phone;
            break;

          case 'ig':
          case 'instagram':
            if (el.tagName === 'A') {
              el.setAttribute('href', site.contact.instagramUrl);
            }
            if (el.getAttribute('data-bind-text') !== null || el.textContent.trim() === '') {
              el.textContent = site.contact.instagram;
            }
            break;

          case 'maps':
            if (el.tagName === 'A') {
              el.setAttribute('href', site.contact.mapsUrl);
            }
            break;

          case 'address':
            el.textContent = site.contact.address;
            break;

          case 'street':
            el.textContent = site.contact.street;
            break;

          case 'city':
            el.textContent = site.contact.city;
            break;

          case 'brand-name':
            el.textContent = site.brand.name;
            break;

          case 'lineage':
            el.textContent = site.brand.lineage;
            break;

          case 'hours-summary':
            el.textContent = site.schedule.hoursSummary;
            break;

          case 'year':
            el.textContent = String(new Date().getFullYear());
            break;

          default:
            // Resolução por caminho de propriedade (ex: "contact.phone", "brand.name")
            var resolvedVal = bindKey.split('.').reduce(function (acc, part) {
              return acc && acc[part] !== undefined ? acc[part] : null;
            }, site);

            if (resolvedVal !== null && resolvedVal !== undefined) {
              if (el.tagName === 'A' && typeof resolvedVal === 'string' && (resolvedVal.startsWith('http') || resolvedVal.startsWith('tel:') || resolvedVal.startsWith('mailto:'))) {
                el.setAttribute('href', resolvedVal);
              } else if (el.tagName === 'IMG') {
                el.setAttribute('src', resolvedVal);
              } else {
                el.textContent = String(resolvedVal);
              }
            }
            break;
        }
      });
    },

    /**
     * Gerenciamento do Menu Mobile
     */
    initMobileMenu: function () {
      var self = this;
      var menuBtns = document.querySelectorAll('.gb-menu-btn, [data-action="toggle-menu"]');
      var mobilePanels = document.querySelectorAll('.gb-mobile-panel, [data-menu-panel]');
      var header = document.querySelector('header, .gb-header');

      if (!menuBtns.length && !mobilePanels.length) return;

      function updateMenuState(open) {
        self.isMenuOpen = open;

        menuBtns.forEach(function (btn) {
          btn.setAttribute('aria-expanded', open ? 'true' : 'false');
          btn.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
          btn.classList.toggle('is-open', open);
        });

        mobilePanels.forEach(function (panel) {
          panel.classList.toggle('is-open', open);
          // Suporte a display inline caso o CSS não tenha regras dedicadas
          if (panel.hasAttribute('hidden') !== null) {
            if (open) {
              panel.removeAttribute('hidden');
            } else {
              panel.setAttribute('hidden', '');
            }
          }
          if (panel.style.display === 'none' && open) {
            panel.style.display = 'flex';
          } else if (panel.style.display === 'flex' && !open) {
            panel.style.display = 'none';
          }
        });

        if (header) {
          header.classList.toggle('is-open', open);
        }
      }

      // Alternar ao clicar no botão
      menuBtns.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
          e.stopPropagation();
          updateMenuState(!self.isMenuOpen);
        });
      });

      // Fechar ao clicar em qualquer link de navegação do painel mobile
      mobilePanels.forEach(function (panel) {
        panel.addEventListener('click', function (e) {
          var targetLink = e.target.closest('a');
          if (targetLink) {
            updateMenuState(false);
          }
        });
      });

      // Fechar com a tecla Escape
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && self.isMenuOpen) {
          updateMenuState(false);
          var firstBtn = menuBtns[0];
          if (firstBtn && typeof firstBtn.focus === 'function') {
            firstBtn.focus();
          }
        }
      });

      // Fechar ao clicar fora do menu
      document.addEventListener('click', function (e) {
        if (!self.isMenuOpen) return;

        var clickedInsideButton = Array.from(menuBtns).some(function (btn) {
          return btn.contains(e.target);
        });
        var clickedInsidePanel = Array.from(mobilePanels).some(function (panel) {
          return panel.contains(e.target);
        });

        if (!clickedInsideButton && !clickedInsidePanel) {
          updateMenuState(false);
        }
      });

      // Métodos públicos para controle externo
      this.toggleMenu = function () { updateMenuState(!self.isMenuOpen); };
      this.openMenu = function () { updateMenuState(true); };
      this.closeMenu = function () { updateMenuState(false); };
    },

    /**
     * Filtro da Grade de Horários (Todos / Gi / No-Gi)
     */
    initScheduleFilter: function () {
      var self = this;
      var filterButtons = document.querySelectorAll('[data-filter]');
      var classCards = document.querySelectorAll('[data-kind]');

      if (!filterButtons.length) return;

      function applyFilter(filterId) {
        self.currentFilter = filterId;

        // Atualiza estado e estilo visual dos botões de filtro
        filterButtons.forEach(function (btn) {
          var isMatch = btn.getAttribute('data-filter') === filterId;
          btn.setAttribute('aria-pressed', isMatch ? 'true' : 'false');
          btn.classList.toggle('is-active', isMatch);

          // Atualização de estilos caso classes CSS dedicadas não estejam presentes
          if (isMatch) {
            btn.style.background = '#FFFFFF';
            btn.style.color = '#0D0F14';
            btn.style.borderColor = '#FFFFFF';
          } else {
            btn.style.background = 'transparent';
            btn.style.color = '#E6E8EC';
            btn.style.borderColor = '#3A4152';
          }
        });

        // Atualiza visibilidade/opacidade dos cards de aula
        classCards.forEach(function (card) {
          var kind = card.getAttribute('data-kind');
          var isVisible = (filterId === 'todos' || kind === filterId);

          card.classList.toggle('is-dimmed', !isVisible);
          card.style.opacity = isVisible ? '1' : '0.25';
          if (!isVisible) {
            card.setAttribute('aria-hidden', 'true');
          } else {
            card.removeAttribute('aria-hidden');
          }
        });
      }

      // Adiciona listeners aos botões de filtro
      filterButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var filterId = btn.getAttribute('data-filter');
          if (filterId) {
            applyFilter(filterId);
          }
        });
      });

      // Aplica o filtro inicial padrão ("todos")
      applyFilter(this.currentFilter);

      // Método público
      this.setFilter = function (filterId) {
        applyFilter(filterId);
      };
    },

    /**
     * Smooth scroll acessível com compensação de altura do header fixo
     */
    initSmoothScroll: function () {
      var self = this;
      var anchorLinks = document.querySelectorAll('a[href^="#"]');

      anchorLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
          var targetId = link.getAttribute('href');
          if (!targetId || targetId === '#') return;

          var targetEl = document.querySelector(targetId);
          if (!targetEl) return;

          e.preventDefault();

          // Fecha menu mobile caso esteja aberto
          if (self.isMenuOpen && typeof self.closeMenu === 'function') {
            self.closeMenu();
          }

          // Calcula altura do header para compensação
          var header = document.querySelector('header, .gb-header');
          var headerHeight = header ? header.getBoundingClientRect().height : 88;

          var elementPosition = targetEl.getBoundingClientRect().top + window.pageYOffset;
          var offsetPosition = elementPosition - headerHeight;

          window.scrollTo({
            top: Math.max(0, offsetPosition),
            behavior: 'smooth'
          });

          // Atualiza hash da URL sem causar salto brusco
          if (window.history && window.history.pushState) {
            window.history.pushState(null, '', targetId);
          } else {
            window.location.hash = targetId;
          }

          // Acessibilidade: transfere o foco para a seção de destino
          targetEl.setAttribute('tabindex', '-1');
          targetEl.focus({ preventScroll: true });
        });
      });
    },

    /**
     * Atualização do ano de copyright no rodapé
     */
    initCurrentYear: function () {
      var currentYear = new Date().getFullYear();
      var yearElements = document.querySelectorAll('[data-year]');
      yearElements.forEach(function (el) {
        el.textContent = String(currentYear);
      });
    }
  };

  // Expor no escopo global
  window.GBApp = GBApp;

  // Inicializar quando o DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      GBApp.init();
    });
  } else {
    GBApp.init();
  }
})();
