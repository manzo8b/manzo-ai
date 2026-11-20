# MANZO AI Academy — Wireframe funzionale Catalogo, Scheda Corso e Modulo
**Versione:** design v1 · **Ambito:** IA, UX learning product, IT/EN/ES · **Stato:** specifica da validare in anteprima, non deploy
**Riferimenti:** `docs/ACADEMY_GLOSSARIO_UI_IT_EN_ES_V1.md`, `academy/catalog-v1.json`, `theme/ACADEMY_CARD_STANDARD.md`, `theme/publish-academy-journeys.py`
**Benchmark strutturale esterno:** https://www.coursera.org/browse e https://www.coursera.org/courses (gerarchie dei prodotti e filtri, NON imitazione della grafica o delle credenziali)

## 1. Percorso di scelta senza carico cognitivo eccessivo

**Domanda di ingresso:** «Cosa vuoi imparare a fare?» — conduce a un obiettivo e al catalogo.
**Gerarchia stabile:** Catalogo Academy → Corso / Base essenziale → Lezione / Laboratorio → Verifica → Passo successivo.
**Due tipi di esperienza:** la selezione per argomento (catalogo) e l'orientamento per obiettivo (tre percorsi guidati già presenti) devono coesistere, senza card ripetute in sezioni concorrenti.

### Catalogo desktop — architettura del primo viewport
```text
[Breadcrumb: Home › Catalogo Academy]                  [Lingue IT · EN · ES]
CATALOGO ACADEMY
Scegli un risultato, non una pagina
[Che cosa vuoi imparare a fare?  ____________________________________]

[Tema ▾]  [Tipo di contenuto ▾]  [Tipo di pratica ▾]  [Lingua ▾] [Azzera filtri]
[15 unità censite*]                        [Ordina: consigliati / titolo]

PERCORSI FORMATIVI                          [9 corsi nel perimetro]
┌───────────────────────────┐ ┌───────────────────────────┐ ┌───────────┐
│ COPERTINA VISIVA          │ │ COPERTINA VISIVA          │ │ ...       │
│ Corso · Tema              │ │ Corso · Tema              │ │           │
│ Titolo leggibile          │ │ Titolo leggibile          │ │           │
│ Saprai...                 │ │ Saprai...                 │ │           │
│ Pratica verificata        │ │ Pratica verificata        │ │           │
│ Lingue effettive          │ │ Lingue effettive          │ │           │
│ [Apri il corso       ↗]   │ │ [Apri il corso       ↗]   │ │           │
└───────────────────────────┘ └───────────────────────────┘ └───────────┘

BASE ESSENZIALE                            [6 moduli fondativi]
[Moduli M01–M06 con titolo, pratica, eventuale laboratorio collegato]

PERCORSI CONSIGLIATI [3 percorsi già esistenti, nessuna copia di card]
LABORATORI E STRUMENTI [directory distinta]
RISORSE E APPROFONDIMENTI [glossari, AI Radar, esercizi, materiali]
```
* 15 = unità principali censite, NON certificazioni né 15 corsi equivalenti.

### Mobile
- Header e breadcrumb compatti, senza sidebar che rubi la larghezza.
- Campo di ricerca con etichetta esplicita; pulsante «Filtri» che espande gli stessi quattro controlli, mai un secondo sistema.
- Una card per riga, copertina leggibile, CTA fissa al fondo della card, nessun testo a tre righe nei pulsanti.
- Nessun carosello che nasconda elementi obbligatori. Filtri persistenti nello stato di navigazione durante la sessione quando realmente implementati; non promettere progresso persistente.

## 2. Regole della card

```text
┌────────────────────────────────────────────────────────────────┐
│ Copertina con codice visivo del tema, colore e microinterazione │
├────────────────────────────────────────────────────────────────┤
│ [Corso]  [Affidabilità e pensiero critico]                      │
│ Allucinazioni IA e verificabilità                               │
│ Al termine saprai distinguere una risposta plausibile da una   │
│ affermazione documentata, usando controlli espliciti            │
│ Laboratorio interattivo + Quiz e verifica                       │
│ Lingue disponibili: IT · EN · ES                                │
│                                       Apri il corso        (↗) │
└────────────────────────────────────────────────────────────────┘
```

**Ordine dati:** tipo > tema > titolo > risultato osservabile > modalità della pratica > lingue realmente disponibili > CTA. 
**Non mostrare:** date di rilascio senza contesto, ore non verificate, presunti voti/stelle, `M02` come titolo, certificazioni simulate.
**Card del modulo fondativo:** stessa anatomia, badge «Modulo fondativo», codice M01 solo secondario, CTA «Apri il modulo». Non descrivere come laboratorio interattivo un esercizio con risposta statica.

## 3. Scheda corso — above the fold

```text
[Catalogo Academy › Affidabilità e pensiero critico › Allucinazioni IA]

[Corso] [Laboratorio interattivo] [IT · EN · ES]
ALLUCINAZIONI IA E VERIFICABILITÀ
Risultato promesso: verifica tre affermazioni e documenta le fonti ...

A chi è rivolto             Cosa saprai fare                 Prima di iniziare
[pubblico verificato]       [2–3 obiettivi osservabili]      [solo prerequisiti verificati]

[Inizia il corso]          [Scopri la pratica]
[NO durata, livello o attestato non attestati]

───────────────────────────────────────────────────────────────
Il programma
01 Conosci  →  02 Sperimenta  →  03 Verifica  →  04 Applica
[sommario reale delle unità, tratto dal contenuto pubblicato]
[prova/verifica descritta per tipo; nessuna iscrizione fittizia]
[fonti, data di aggiornamento delle fonti, limiti e disponibilità lingua]

[Passo successivo: collegamento reale a lezione o laboratorio]
```

Se si apre un modulo M01–M06, l'H1 resta il titolo descrittivo; il codice è `Modulo fondativo · M02`. Se lo studio è esterno alla pagina, usare «Apri lo studio collegato» e un URL verificato. Se non esiste, usare «Attività nella lezione» senza CTA inesistente.

## 4. Breadcrumb verificabile e prossimo passo

- Livello 1: Home › Catalogo Academy
- Livello 2: Catalogo Academy › Corso › Programma (nomi di display localizzati)
- Livello 3: Catalogo Academy › Corso › Modulo N o Laboratorio N
- In ogni lezione scegliere UNA CTA primaria in fondo, con priorità: laboratorio realmente collegato → verifica in pagina → unità seguente → ritorno al catalogo.
- Un collegamento a URL diverso di lingua deve esplicitarlo («Apri il corso in italiano»). Mai cambiare il locale senza avviso.
- Collegamenti verso altre unità sono contestuali («Può interessarti») e secondari; evitare doppi ingressi non giustificati.

## 5. Filtri e modello dati

Filtri: (1) **Tema** (cinque macro-aree), (2) **Tipo** (Corso / Modulo fondativo / Laboratorio / Risorsa), (3) **Pratica** (Interattiva / Guidata / Quiz e verifica / Nessun laboratorio dedicato), (4) **Lingua** (IT/EN/ES), con combinazione AND fra criteri e OR nelle modalità di pratica solo se esplicitato.

Per il primo rilascio del catalogo, i 15 record canonici sono in `academy/catalog-v1.json`. Laboratori autonomi e risorse entrano successivamente come record aggiuntivi con il proprio ID e una relazione `part_of` o `related_to`; non creare duplicati dei corsi per renderli in più sezioni.

Campi obbligatori per la card navigabile: ID canonico, tipo, tema, titolo locale verificato, URL stesso locale pubblicato, obiettivo dichiarato e verificato, pratica verificata, disponibilità linguistica. Dove manca un dato, **omettere l'etichetta o mostrare «Da verificare» internamente**, non inventare.
 
## 6. QA di accettazione della successiva implementazione

1. Un solo risultato per `id`, anche se mostrato in più categorie attraverso filtri
2. Filtri tastiera/mobile, un solo stato aggiornato, pulsante reset, annunci accessibili dei risultati
3. Tutti i link risolti nella build; la lingua scelta non deve indirizzare a una pagina non pubblicata
4. AI Teaching Lab EN/ES non produce falsa equivalenza: l'accesso italiano deve essere esplicito
5. Card della Home e Academy condividono stile/geometria/CTA; niente regressione del menu delle lingue o della scatola magica
6. Nessun punto finale sui titoli e nessun badge inutile
7. Test 375, 768, 1440 px e Safari/iPhone, reduced-motion e focus
8. Risultati di apprendimento e laboratori non dichiarati disponibili se non dimostrati

## 7. Sequenza di implementazione proposta

**S1** — validare glossario e manifest, registrare rotte certe e route_missing senza falsi link  
**S2** — catalogo Academy unificato in anteprima (non cancellare i tre percorsi guidati già presenti)  
**S3** — scheda corso pilota: Allucinazioni IA, perché contenuto, pratica e tre lingue risultano disponibili  
**S4** — aggiungere breadcrumb + passo successivo nei moduli M01–M06, inizialmente senza inventare laboratori  
**S5** — colmare laboratori M02/M04/M05/M06 con progettazione didattica distinta, dopo verifica  
**S6** — collaudo e rilascio incrementale; non deploy commerciale SaaS
