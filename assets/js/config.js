/**
 * Gracie Barra São Mateus — Configurações Globais
 * 
 * Este arquivo centraliza todas as informações editáveis do site:
 * contatos, redes sociais, grade de horários, cores e textos institucionais.
 * 
 * Para atualizar o WhatsApp, endereço ou horários da academia,
 * basta editar os valores deste arquivo.
 */

(function () {
  'use strict';

  var phoneFormatted = '(27) 99949-4456';
  var phoneRaw = '5527999494456';
  var defaultWaMessage = 'Olá! Quero agendar uma aula experimental na Gracie Barra São Mateus.';
  var waUrl = 'https://wa.me/' + phoneRaw + '?text=' + encodeURIComponent(defaultWaMessage);
  var igUser = '@gbsaomateus_prof_mucio_maia';
  var igUrl = 'https://www.instagram.com/gbsaomateus_prof_mucio_maia/';
  var mapsUrl = 'https://share.google/cw5yoKluPTkqPXMPN';

  var SITE = {
    // Informações da marca e franquia
    brand: {
      name: 'Gracie Barra São Mateus',
      shortName: 'GB São Mateus',
      slogan: 'Jiu-Jitsu para todos',
      description: 'Jiu-Jitsu para todos. Gi, No-Gi, turma kids e turma feminina em Guriri, São Mateus.',
      neighborhood: 'Guriri Norte',
      city: 'Guriri, São Mateus – ES',
      state: 'Espírito Santo',
      lineage: 'Mestre Carlos Gracie Jr. → Mestre Vinicius Draculino → Mestre Múcio Maia',
      headInstructor: 'Mestre Múcio Maia',
      rank: 'Faixa preta · Gracie Barra',
      schoolBadge: 'SÃO MATEUS · ES'
    },

    // Identidade visual / Cores do design system
    theme: {
      accent: '#D7182A',       // Vermelho oficial GB
      accentLight: '#FF4D5A',  // Vermelho destaque / hover
      blue: '#0B3D91',         // Azul oficial GB
      bg: '#0D0F14',           // Fundo principal escuro
      surface: '#151925',      // Superfície cartões / containers
      surfaceAlt: '#1C2231',   // Superfície horários / itens
      card: '#FFFFFF',         // Superfície clara
      text: '#11141B',         // Texto escuro
      textLight: '#FFFFFF',    // Texto claro
      muted: '#3A4150',        // Texto secundário escuro
      mutedLight: '#A9B0BE',   // Texto secundário claro
      border: '#222838',       // Borda escura
      borderLight: '#E1E4EA'   // Borda clara
    },

    // Informações de contato e localização
    contact: {
      phone: phoneFormatted,
      phoneRaw: phoneRaw,
      whatsapp: phoneRaw,
      whatsappFormatted: phoneFormatted,
      whatsappMsg: defaultWaMessage,
      whatsappUrl: waUrl,
      instagram: igUser,
      instagramUrl: igUrl,
      street: 'Rua Professor Amaro Nascimento Mendes (antiga Rua 7), nº 351',
      neighborhood: 'Guriri Norte',
      cityState: 'São Mateus – ES',
      address: 'Rua Professor Amaro Nascimento Mendes (antiga Rua 7), nº 351, Guriri Norte, São Mateus – ES',
      mapsUrl: mapsUrl,
      displayHours: 'Segunda a sexta: 09:30 · 16:30 · 19:30'
    },

    // Grade semanal de treinos e modalidades
    schedule: {
      kinds: {
        gi: {
          id: 'gi',
          label: 'GI',
          fullName: 'Jiu-Jitsu Gi',
          desc: 'Com kimono',
          bg: '#0B3D91',
          color: '#FFFFFF'
        },
        nogi: {
          id: 'nogi',
          label: 'NO-GI',
          fullName: 'Jiu-Jitsu No-Gi',
          desc: 'Sem kimono',
          bg: '#D7182A',
          color: '#FFFFFF'
        }
      },
      filters: [
        { id: 'todos', label: 'Todos' },
        { id: 'gi', label: 'Gi · com kimono' },
        { id: 'nogi', label: 'No-Gi · sem kimono' }
      ],
      days: [
        {
          name: 'Segunda',
          shortName: 'Seg',
          classes: [
            { time: '16:30', kind: 'gi', label: 'GI', desc: 'Com kimono', bg: '#0B3D91' },
            { time: '19:30', kind: 'gi', label: 'GI', desc: 'Com kimono', bg: '#0B3D91' }
          ]
        },
        {
          name: 'Terça',
          shortName: 'Ter',
          classes: [
            { time: '09:30', kind: 'gi', label: 'GI', desc: 'Com kimono', bg: '#0B3D91' }
          ]
        },
        {
          name: 'Quarta',
          shortName: 'Qua',
          classes: [
            { time: '16:30', kind: 'gi', label: 'GI', desc: 'Com kimono', bg: '#0B3D91' },
            { time: '19:30', kind: 'gi', label: 'GI', desc: 'Com kimono', bg: '#0B3D91' }
          ]
        },
        {
          name: 'Quinta',
          shortName: 'Qui',
          classes: [
            { time: '09:30', kind: 'gi', label: 'GI', desc: 'Com kimono', bg: '#0B3D91' },
            { time: '16:30', kind: 'nogi', label: 'NO-GI', desc: 'Sem kimono', bg: '#D7182A' },
            { time: '19:30', kind: 'nogi', label: 'NO-GI', desc: 'Sem kimono', bg: '#D7182A' }
          ]
        },
        {
          name: 'Sexta',
          shortName: 'Sex',
          classes: [
            { time: '16:30', kind: 'gi', label: 'GI', desc: 'Com kimono', bg: '#0B3D91' },
            { time: '19:30', kind: 'gi', label: 'GI', desc: 'Com kimono', bg: '#0B3D91' }
          ]
        }
      ],
      notice: 'Turma Kids e Turma Feminina têm horários próprios. Consulte pelo WhatsApp.',
      hoursSummary: '09:30 · 16:30 · 19:30',
      daysSummary: 'Segunda a sexta'
    },

    // Conteúdo institucional estruturado
    content: {
      professor: {
        name: 'Mestre Múcio Maia',
        rank: 'Faixa preta · Gracie Barra',
        bio: 'Professor e competidor, Múcio Maia está à frente da Gracie Barra São Mateus. No tatame, une a metodologia Gracie Barra à experiência de quem compete: aula organizada, atenção a cada aluno e um caminho claro do primeiro treino à faixa preta.',
        titles: [
          {
            year: '2022',
            title: 'Emanuel Amâncio — campeão peso pena (sub-70 kg)',
            event: 'AJP Tour Guarapari International · atleta treinado pelo Mestre Múcio'
          },
          {
            year: '2018',
            title: 'Múcio Maia — vice-campeão faixa preta, peso leve',
            event: 'Belo Horizonte Winter Open · CBJJ'
          },
          {
            year: '2018',
            title: 'Thays Scampale — bronze faixa azul, peso leve',
            event: 'Belo Horizonte Winter Open · CBJJ'
          }
        ]
      },
      modalities: [
        {
          id: 'gi',
          title: 'Jiu-Jitsu Gi',
          subtitle: 'Com kimono',
          description: 'A essência do Jiu-Jitsu tradicional Gracie Barra. Estruturado em fundamentos sólidos, defesa pessoal e evolução técnica contínua para iniciantes e graduados.'
        },
        {
          id: 'nogi',
          title: 'Jiu-Jitsu No-Gi',
          subtitle: 'Sem kimono',
          description: 'Treino dinâmico em ritmo acelerado com rashguard e bermuda. Foco em controle de pegadas corporais, transições ágeis e finalizações.'
        },
        {
          id: 'kids',
          title: 'GB Kids',
          subtitle: 'Infantil',
          description: 'Programa pedagógico focado em disciplina, respeito, foco, autoconfiança e desenvolvimento motor de crianças e jovens em ambiente seguro e motivador.'
        },
        {
          id: 'feminina',
          title: 'Turma Feminina',
          subtitle: 'Exclusiva para mulheres',
          description: 'Espaço acolhedor e dedicado ao público feminino, unindo técnicas eficazes de defesa pessoal, condicionamento físico de alto rendimento e fortalecimento mútuo.'
        }
      ]
    }
  };

  // Expor no escopo global
  window.SITE = SITE;
})();
