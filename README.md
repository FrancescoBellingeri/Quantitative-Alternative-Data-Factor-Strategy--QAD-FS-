Pilastri fondamentali della strategia QAD-FS, definiti punto per punto.

1. La Filosofia di Investimento (L'Obiettivo)
   Obiettivo: Generare un rendimento positivo e decorrelato dall'andamento del mercato azionario (Alpha), sfruttando inefficienze informative tramite l'analisi quantitativa di dati tradizionali e alternativi.

Approccio: Sistematico, basato su regole, non discrezionale. Le decisioni di acquisto e vendita sono determinate al 100% dal modello matematico.

Stile: Equity Long/Short, Market-Neutral.

2. L'Universo di Investimento (Il Campo da Gioco)
   Quali titoli: Azioni a grande capitalizzazione e alta liquidità.

Esempio Pratico: L'indice S&P 500 (per il mercato USA) o lo STOXX Europe 600 (per il mercato europeo).

Perché: Dati abbondanti e affidabili, alta liquidità che riduce i costi di transazione e permette di aprire posizioni short facilmente. Non vogliamo avere a che fare con small caps illiquide.

3. I Dati (Le Materie Prime)
   Questa è la parte cruciale. La strategia si nutre di dati, che divideremo in due categorie:

Dati Tradizionali (la base):

Dati di Mercato: Prezzi giornalieri, volumi di scambio.

Dati Fondamentali: Dati di bilancio trimestrali (es. ricavi, utili, stato patrimoniale) da cui deriviamo i "multipli" (P/E, P/B, EV/EBITDA, etc.) e indicatori di qualità (ROE, ROA, Leva Finanziaria).

Dati Alternativi (il nostro "edge", l'ingrediente segreto):

Sentiment delle News Finanziarie: Per ogni società nell'universo, ogni giorno, calcoliamo un punteggio di sentiment (da -1, molto negativo, a +1, molto positivo) basato sul tono degli articoli pubblicati dalle principali agenzie di stampa (es. Reuters, Bloomberg, Wall Street Journal). Esistono provider di dati che forniscono questo punteggio già calcolato, oppure (per la sua tesi) può essere costruito usando tecniche di NLP.

4. I Fattori (I Segnali di Trading)
   I dati grezzi sono inutili. Dobbiamo trasformarli in "fattori", ovvero segnali standardizzati che ci dicono se un'azione è "attraente" o "non attraente". Ecco i fattori che useremo:

Fattore 1: Value (Quanto è "a buon mercato"?): Un punteggio combinato basato su Earnings Yield (E/P), Book-to-Market (B/P) e Free Cash Flow Yield.

Fattore 2: Momentum (Qual è il trend?): Performance del titolo negli ultimi 12 mesi, escludendo l'ultimo mese.

Fattore 3: Quality (L'azienda è solida?): Un punteggio combinato basato su Return on Equity (ROE), basso Debt-to-Equity e stabilità degli utili.

Fattore 4: News Sentiment (Cosa dice la stampa?): Media mobile a 30 giorni del punteggio di sentiment delle news. Un punteggio alto indica notizie persistentemente positive.

Fattore 5: Sentiment Momentum (Il sentiment sta migliorando?): La variazione della media mobile del sentiment a 7 giorni rispetto a quella a 30 giorni. Questo cattura i cambiamenti nel tono delle notizie, che spesso sono più predittivi del livello assoluto.

5. Il Modello (Il Cervello Decisionale)
   Il modello non predice il prezzo, ma fa una cosa più semplice e robusta: impara a distinguere i futuri vincitori dai futuri perdenti.

Obiettivo del Modello: Ogni mese, per ogni azione dell'universo, generare un singolo "Punteggio di Attrattività" da 0 a 1.

Input (Features): I valori normalizzati dei 5 fattori che abbiamo definito sopra.

Output (Target da "imparare"): Il rendimento del titolo nel mese successivo, aggiustato per il rischio di mercato.

Algoritmo: Gradient Boosted Trees (es. XGBoost). È il gold standard per questo tipo di problemi. È un algoritmo potente che può catturare relazioni complesse e non lineari tra i fattori e i rendimenti futuri.

6. Il Processo Operativo (La Ricetta Mese per Mese)
   Ecco cosa fa la strategia, come un orologio, il primo giorno di ogni mese:

Raccolta Dati: Acquisisce tutti i dati (tradizionali e alternativi) aggiornati all'ultimo giorno del mese precedente.

Calcolo Fattori: Calcola i valori aggiornati dei 5 fattori per ogni titolo dell'S&P 500.

Esecuzione Modello: Fornisce i fattori in input al modello XGBoost pre-allenato. Il modello produce il "Punteggio di Attrattività" per tutti i 500 titoli.

Ranking: Ordina i 500 titoli dal punteggio più alto al più basso.

Costruzione Portafoglio:

POSIZIONE LONG: Acquista i 50 titoli con il punteggio più alto (il primo decile).

POSIZIONE SHORT: Vende allo scoperto i 50 titoli con il punteggio più basso (l'ultimo decile).

Ponderazione: Per semplicità, ogni posizione ha lo stesso peso (Equal Weight).

Neutralizzazione del Rischio (Hedging):

Calcola il Beta totale del portafoglio Long e del portafoglio Short.

Apre una posizione su un future dell'indice (es. E-mini S&P 500) per assicurarsi che il Beta netto del portafoglio complessivo sia zero. Se il portafoglio ha un Beta residuo positivo, si shorta il future; se è negativo, si compra il future.

Mantenimento e Ribilanciamento: La posizione viene mantenuta per un mese intero. Il primo giorno del mese successivo, si liquida l'intero portafoglio e si ripete il processo dal punto 1.

Esempio Concreto
È il 1° Dicembre.

Il modello analizza i dati fino al 30 Novembre.

Apple Inc. ottiene un punteggio di 0.92 (si classifica 8° su 500).

Azienda Manifatturiera XYZ ottiene un punteggio di 0.15 (si classifica 485° su 500).

La strategia compra Apple e vende allo scoperto XYZ.

I Comandamenti del Quant (Consigli Operativi)
Non sbirciare il futuro (Lookahead Bias): Assicurati che le decisioni prese al giorno T usino SOLO dati disponibili fino al giorno T. È l'errore più comune e mortale.

I costi contano: Il backtest deve includere stime realistiche per commissioni, slippage (differenza tra prezzo atteso ed eseguito) e costi per prendere a prestito i titoli da shortare.

I modelli invecchiano: Il modello deve essere ri-allenato periodicamente (es. ogni anno) su dati nuovi per adattarsi a cambiamenti nelle condizioni di mercato.
