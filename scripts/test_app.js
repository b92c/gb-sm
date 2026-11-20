/**
 * Test harness for config.js and app.js in simulated DOM environment
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function runTests() {
  console.log('------------------------------------------------------------');
  console.log('EXECUTING JS RUNTIME AUDIT (config.js & app.js)');
  console.log('------------------------------------------------------------');

  const configCode = fs.readFileSync(path.join(__dirname, '../assets/js/config.js'), 'utf-8');
  const appCode = fs.readFileSync(path.join(__dirname, '../assets/js/app.js'), 'utf-8');

  // Minimal DOM Node implementation
  class DOMTokenList {
    constructor() {
      this._set = new Set();
    }
    add(cls) { this._set.add(cls); }
    remove(cls) { this._set.delete(cls); }
    toggle(cls, force) {
      if (force === true) { this._set.add(cls); return true; }
      if (force === false) { this._set.delete(cls); return false; }
      if (this._set.has(cls)) { this._set.delete(cls); return false; }
      this._set.add(cls); return true;
    }
    contains(cls) { return this._set.has(cls); }
    toString() { return Array.from(this._set).join(' '); }
  }

  class MockElement {
    constructor(tagName, id = '', className = '', attrs = {}) {
      this.tagName = tagName.toUpperCase();
      this.id = id;
      this.classList = new DOMTokenList();
      if (className) {
        className.split(/\s+/).filter(Boolean).forEach(c => this.classList.add(c));
      }
      this.attributes = { ...attrs };
      if (id) this.attributes.id = id;
      this.style = {};
      this.listeners = {};
      this.textContent = attrs.textContent || '';
      this.children = [];
      this.parentElement = null;
    }

    getAttribute(name) {
      if (name === 'class') return this.classList.toString();
      return this.attributes[name] !== undefined ? this.attributes[name] : null;
    }

    setAttribute(name, val) {
      this.attributes[name] = String(val);
      if (name === 'class') {
        this.classList = new DOMTokenList();
        String(val).split(/\s+/).filter(Boolean).forEach(c => this.classList.add(c));
      }
    }

    removeAttribute(name) {
      delete this.attributes[name];
    }

    hasAttribute(name) {
      return this.attributes[name] !== undefined;
    }

    addEventListener(event, fn) {
      if (!this.listeners[event]) this.listeners[event] = [];
      this.listeners[event].push(fn);
    }

    dispatchEvent(event) {
      if (!event.target) event.target = this;
      if (this.listeners[event.type]) {
        for (const fn of this.listeners[event.type]) {
          fn(event);
        }
      }
      if (this.parentElement && !event.propagationStopped) {
        this.parentElement.dispatchEvent(event);
      }
    }

    appendChild(child) {
      child.parentElement = this;
      this.children.push(child);
      return child;
    }

    contains(other) {
      if (other === this) return true;
      for (const child of this.children) {
        if (child.contains(other)) return true;
      }
      return false;
    }

    closest(selector) {
      let current = this;
      while (current) {
        if (current.matches && current.matches(selector)) return current;
        current = current.parentElement;
      }
      return null;
    }

    matches(selector) {
      if (selector === 'a') return this.tagName === 'A';
      if (selector.startsWith('#')) return this.id === selector.slice(1);
      if (selector.startsWith('.')) return this.classList.contains(selector.slice(1));
      return false;
    }

    focus(opts) {
      this.isFocused = true;
      this.focusOpts = opts;
    }

    getBoundingClientRect() {
      return { top: 150, height: 76, width: 1200 };
    }
  }

  // Build simulated DOM matching index.html
  const header = new MockElement('header', 'site-header', 'site-header');
  const menuBtn = new MockElement('button', 'gb-menu-toggle', 'gb-menu-btn', {
    type: 'button',
    'aria-label': 'Abrir menu',
    'aria-expanded': 'false',
    'aria-controls': 'mobile-menu'
  });
  const mobilePanel = new MockElement('nav', 'mobile-menu', 'gb-mobile-panel', {
    'aria-label': 'Menu móvel'
  });
  const mobileLink1 = new MockElement('a', '', 'gb-link', { href: '#sobre', textContent: 'A academia' });
  const mobileLink2 = new MockElement('a', '', 'gb-link', { href: '#horarios', textContent: 'Horários' });
  mobilePanel.appendChild(mobileLink1);
  mobilePanel.appendChild(mobileLink2);

  header.appendChild(menuBtn);
  header.appendChild(mobilePanel);

  // Filter buttons
  const btnFilterTodos = new MockElement('button', '', 'gb-filter-btn is-active', {
    'data-filter': 'todos',
    'aria-pressed': 'true',
    textContent: 'Todos'
  });
  const btnFilterGi = new MockElement('button', '', 'gb-filter-btn', {
    'data-filter': 'gi',
    'aria-pressed': 'false',
    textContent: 'Gi'
  });
  const btnFilterNogi = new MockElement('button', '', 'gb-filter-btn', {
    'data-filter': 'nogi',
    'aria-pressed': 'false',
    textContent: 'No-Gi'
  });

  // Schedule cards (8 gi, 2 nogi)
  const cards = [];
  for (let i = 0; i < 8; i++) {
    cards.push(new MockElement('div', `card-gi-${i}`, 'gb-card', { 'data-kind': 'gi' }));
  }
  for (let i = 0; i < 2; i++) {
    cards.push(new MockElement('div', `card-nogi-${i}`, 'gb-card', { 'data-kind': 'nogi' }));
  }

  // Data bind elements
  const waLink = new MockElement('a', 'wa-cta', 'gb-btn', {
    'data-bind': 'wa',
    href: 'https://wa.me/5527999494456?text=fallback',
    textContent: 'Aula experimental'
  });
  const igLink = new MockElement('a', 'ig-cta', 'gb-link', {
    'data-bind': 'ig',
    href: 'https://www.instagram.com/fallback',
    textContent: 'Instagram'
  });
  const mapsLink = new MockElement('a', 'maps-cta', 'gb-link', {
    'data-bind': 'maps',
    href: 'https://share.google/fallback',
    textContent: 'Localização'
  });
  const addressSpan = new MockElement('span', 'address-span', '', {
    'data-bind': 'address',
    textContent: 'Placeholder Endereço'
  });
  const yearSpan = new MockElement('span', 'year-span', '', {
    'data-year': '',
    textContent: '2020'
  });

  // Anchor targets
  const sectionInicio = new MockElement('section', 'inicio', '');
  const sectionSobre = new MockElement('section', 'sobre', '');
  const sectionModalidades = new MockElement('section', 'modalidades', '');
  const sectionHorarios = new MockElement('section', 'horarios', '');
  const sectionProfessor = new MockElement('section', 'professor', '');
  const sectionContato = new MockElement('section', 'contato', '');

  const allElements = [
    header, menuBtn, mobilePanel, mobileLink1, mobileLink2,
    btnFilterTodos, btnFilterGi, btnFilterNogi,
    ...cards,
    waLink, igLink, mapsLink, addressSpan, yearSpan,
    sectionInicio, sectionSobre, sectionModalidades, sectionHorarios, sectionProfessor, sectionContato
  ];

  // Mock document and window
  const documentListeners = {};
  const mockDocument = {
    readyState: 'complete',
    addEventListener: (ev, fn) => {
      if (!documentListeners[ev]) documentListeners[ev] = [];
      documentListeners[ev].push(fn);
    },
    dispatchEvent: (ev) => {
      if (documentListeners[ev.type]) {
        for (const fn of documentListeners[ev.type]) fn(ev);
      }
    },
    querySelectorAll: (sel) => {
      if (sel === '[data-bind]') return [waLink, igLink, mapsLink, addressSpan];
      if (sel === '.gb-menu-btn, [data-action="toggle-menu"]') return [menuBtn];
      if (sel === '.gb-mobile-panel, [data-menu-panel]') return [mobilePanel];
      if (sel === '[data-filter]') return [btnFilterTodos, btnFilterGi, btnFilterNogi];
      if (sel === '[data-kind]') return cards;
      if (sel === 'a[href^="#"]') return [mobileLink1, mobileLink2];
      if (sel === '[data-year]') return [yearSpan];
      return [];
    },
    querySelector: (sel) => {
      if (sel === 'header, .gb-header') return header;
      if (sel === '#sobre') return sectionSobre;
      if (sel === '#horarios') return sectionHorarios;
      if (sel === '#inicio') return sectionInicio;
      if (sel === '#modalidades') return sectionModalidades;
      if (sel === '#professor') return sectionProfessor;
      if (sel === '#contato') return sectionContato;
      return null;
    }
  };

  const mockWindow = {
    document: mockDocument,
    scrollTo: (opts) => { mockWindow.lastScroll = opts; },
    pageYOffset: 0,
    history: {
      pushState: (state, title, hash) => { mockWindow.lastHash = hash; }
    }
  };

  const sandbox = {
    window: mockWindow,
    document: mockDocument,
    console: console,
    Date: Date,
    encodeURIComponent: encodeURIComponent,
    String: String,
    Array: Array
  };
  vm.createContext(sandbox);

  // Step 1: Run config.js
  vm.runInContext(configCode, sandbox);
  const SITE = sandbox.window.SITE;
  if (!SITE || !SITE.brand || !SITE.contact || !SITE.schedule) {
    throw new Error('config.js failed to export valid SITE object!');
  }
  console.log('✓ config.js executed successfully');
  console.log(`  - Brand: ${SITE.brand.name}`);
  console.log(`  - Phone: ${SITE.contact.phone}`);
  console.log(`  - WhatsApp URL: ${SITE.contact.whatsappUrl}`);
  console.log(`  - Instagram URL: ${SITE.contact.instagramUrl}`);
  console.log(`  - Maps URL: ${SITE.contact.mapsUrl}`);
  console.log(`  - Schedule: ${SITE.schedule.days.length} days defined`);

  // Step 2: Run app.js
  vm.runInContext(appCode, sandbox);
  const GBApp = sandbox.window.GBApp;
  if (!GBApp) {
    throw new Error('app.js failed to export GBApp!');
  }
  console.log('✓ app.js initialized successfully (GBApp object present)');

  // Test 1: Data-binding
  console.log('\nTesting Data-Binding:');
  if (waLink.getAttribute('href') !== SITE.contact.whatsappUrl) {
    throw new Error(`waLink href mismatch: expected ${SITE.contact.whatsappUrl}, got ${waLink.getAttribute('href')}`);
  }
  console.log('✓ WhatsApp href data-bound correctly');

  if (igLink.getAttribute('href') !== SITE.contact.instagramUrl) {
    throw new Error(`igLink href mismatch: expected ${SITE.contact.instagramUrl}, got ${igLink.getAttribute('href')}`);
  }
  console.log('✓ Instagram href data-bound correctly');

  if (mapsLink.getAttribute('href') !== SITE.contact.mapsUrl) {
    throw new Error(`mapsLink href mismatch: expected ${SITE.contact.mapsUrl}, got ${mapsLink.getAttribute('href')}`);
  }
  console.log('✓ Google Maps href data-bound correctly');

  if (addressSpan.textContent !== SITE.contact.address) {
    throw new Error(`addressSpan textContent mismatch`);
  }
  console.log('✓ Address span textContent data-bound correctly');

  if (yearSpan.textContent !== String(new Date().getFullYear())) {
    throw new Error(`yearSpan textContent mismatch: expected current year`);
  }
  console.log(`✓ Copyright year data-bound to ${yearSpan.textContent}`);

  // Test 2: Mobile Menu
  console.log('\nTesting Mobile Menu Interactions:');
  if (GBApp.isMenuOpen !== false || menuBtn.getAttribute('aria-expanded') !== 'false') {
    throw new Error('Initial menu state is not closed');
  }
  console.log('✓ Menu starts in closed state (aria-expanded="false")');

  // Click to open
  menuBtn.dispatchEvent({ type: 'click', stopPropagation: () => {} });
  if (GBApp.isMenuOpen !== true || menuBtn.getAttribute('aria-expanded') !== 'true' || !header.classList.contains('is-open')) {
    throw new Error('Menu failed to open on button click');
  }
  console.log('✓ Menu opens on button click (is-open applied to header, aria-expanded="true")');

  // Click outside to close
  const outsideEl = new MockElement('div', 'outside');
  mockDocument.dispatchEvent({ type: 'click', target: outsideEl });
  if (GBApp.isMenuOpen !== false || menuBtn.getAttribute('aria-expanded') !== 'false') {
    throw new Error('Menu failed to close on click outside');
  }
  console.log('✓ Menu closes on click outside');

  // Open again and close with Escape
  menuBtn.dispatchEvent({ type: 'click', stopPropagation: () => {} });
  mockDocument.dispatchEvent({ type: 'keydown', key: 'Escape' });
  if (GBApp.isMenuOpen !== false || menuBtn.getAttribute('aria-expanded') !== 'false' || !menuBtn.isFocused) {
    throw new Error('Menu failed to close on Escape key or failed to restore focus');
  }
  console.log('✓ Menu closes on Escape key and restores focus to menu button');

  // Open again and close by clicking navigation link inside panel
  menuBtn.dispatchEvent({ type: 'click', stopPropagation: () => {} });
  mobilePanel.dispatchEvent({ type: 'click', target: mobileLink1 });
  if (GBApp.isMenuOpen !== false) {
    throw new Error('Menu failed to close when clicking a link inside the panel');
  }
  console.log('✓ Menu closes when navigation link inside panel is clicked');

  // Test 3: Schedule Filter
  console.log('\nTesting Schedule Filter:');
  // Initial filter is 'todos'
  if (btnFilterTodos.getAttribute('aria-pressed') !== 'true' || btnFilterGi.getAttribute('aria-pressed') !== 'false') {
    throw new Error('Default filter is not "todos"');
  }
  cards.forEach(c => {
    if (c.classList.contains('is-dimmed') || c.style.opacity !== '1') {
      throw new Error('All cards should be visible in "todos" mode');
    }
  });
  console.log('✓ "Todos" filter active by default (10/10 cards visible, opacity 1, no .is-dimmed)');

  // Filter "Gi"
  btnFilterGi.dispatchEvent({ type: 'click' });
  if (btnFilterGi.getAttribute('aria-pressed') !== 'true' || btnFilterTodos.getAttribute('aria-pressed') !== 'false') {
    throw new Error('Filter Gi button aria-pressed not updated');
  }
  cards.filter(c => c.getAttribute('data-kind') === 'gi').forEach(c => {
    if (c.classList.contains('is-dimmed') || c.style.opacity !== '1') {
      throw new Error('Gi cards should be visible in Gi filter');
    }
  });
  cards.filter(c => c.getAttribute('data-kind') === 'nogi').forEach(c => {
    if (!c.classList.contains('is-dimmed') || c.style.opacity !== '0.25' || c.getAttribute('aria-hidden') !== 'true') {
      throw new Error('No-Gi cards should be dimmed with aria-hidden in Gi filter');
    }
  });
  console.log('✓ "Gi" filter applied correctly: 8 Gi cards visible, 2 No-Gi cards dimmed (opacity 0.25, .is-dimmed, aria-hidden="true")');

  // Filter "No-Gi"
  btnFilterNogi.dispatchEvent({ type: 'click' });
  cards.filter(c => c.getAttribute('data-kind') === 'nogi').forEach(c => {
    if (c.classList.contains('is-dimmed') || c.style.opacity !== '1' || c.hasAttribute('aria-hidden')) {
      throw new Error('No-Gi cards should be visible in No-Gi filter');
    }
  });
  cards.filter(c => c.getAttribute('data-kind') === 'gi').forEach(c => {
    if (!c.classList.contains('is-dimmed') || c.style.opacity !== '0.25' || c.getAttribute('aria-hidden') !== 'true') {
      throw new Error('Gi cards should be dimmed in No-Gi filter');
    }
  });
  console.log('✓ "No-Gi" filter applied correctly: 2 No-Gi cards visible, 8 Gi cards dimmed (opacity 0.25, .is-dimmed, aria-hidden="true")');

  // Reset to "Todos"
  btnFilterTodos.dispatchEvent({ type: 'click' });
  cards.forEach(c => {
    if (c.classList.contains('is-dimmed') || c.style.opacity !== '1' || c.hasAttribute('aria-hidden')) {
      throw new Error('All cards should be visible after resetting to Todos');
    }
  });
  console.log('✓ Reset to "Todos" restores all 10 cards perfectly');

  // Test 4: Smooth Scroll
  console.log('\nTesting Smooth Scroll:');
  let defaultPrevented = false;
  mobileLink1.dispatchEvent({
    type: 'click',
    preventDefault: () => { defaultPrevented = true; }
  });
  if (!defaultPrevented || mockWindow.lastHash !== '#sobre' || !sectionSobre.isFocused || sectionSobre.getAttribute('tabindex') !== '-1') {
    throw new Error('Smooth scroll failed to handle link click properly');
  }
  console.log('✓ Anchor click prevents default, updates hash to #sobre, sets tabindex="-1", and focuses target element');

  console.log('\n============================================================');
  console.log('ALL JS RUNTIME TESTS PASSED WITH ZERO ERRORS (100% SUCCESS)');
  console.log('============================================================\n');
}

runTests();
