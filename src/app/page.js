const collaborationSteps = [
  {
    title: '1. Strategia inwestorska',
    text: 'Waliduję model inwestycji: budżet, harmonogram, ryzyka i KPI zanim ruszy wykonanie.',
  },
  {
    title: '2. Dowóz kontraktowy',
    text: 'DEMOCO otrzymuje klarowny zakres, realistyczny plan i szybkie decyzje operacyjne.',
  },
  {
    title: '3. Wspólna egzekucja',
    text: 'Prowadzę weekly steering, claim prevention i kontrolę cashflow po obu stronach stołu.',
  },
  {
    title: '4. Wynik biznesowy',
    text: 'Inwestor dostaje projekt na czas, wykonawca rentowność, a relacja zostaje na kolejne inwestycje.',
  },
]

const advantages = [
  '18+ lat doświadczenia w projektach mieszkaniowych i komercyjnych',
  'Łączenie perspektywy inwestora, generalnego wykonawcy i zarządzania kontraktem',
  'Skuteczne porządkowanie projektów zagrożonych opóźnieniem lub przekroczeniem budżetu',
  'Mocny nacisk na komunikację, transparentność i szybkie decyzje',
]

export default function Home() {
  return (
    <main>
      <section className="hero">
        <p className="tag">Prezentacja współpracy inwestor ↔ generalny wykonawca</p>
        <h1>DEMOCO × Hildebrandt Management</h1>
        <p className="lead">
          Zamieniam napięcie między inwestorem a wykonawcą w przewagę projektową:
          lepszą kontrolę kosztów, krótsze ścieżki decyzyjne i przewidywalny wynik inwestycji.
        </p>
      </section>

      <section>
        <h2>Kim jestem dla tego układu?</h2>
        <p>
          Jestem partnerem, który spina strategię inwestora z realiami placu budowy.
          Wchodzę tam, gdzie projekty potrzebują leadershipu, porządku operacyjnego i
          twardego dowożenia efektu biznesowego.
        </p>
        <ul className="checklist">
          {advantages.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Dlaczego DEMOCO?</h2>
        <p>
          DEMOCO ma DNA wykonawcze i kulturę odpowiedzialności za wynik. To idealny
          partner dla inwestora, który oczekuje nie tylko budowy, ale sprawnego delivery
          całej inwestycji od startu do odbiorów.
        </p>
        <div className="pillRow">
          <span>Jakość wykonania</span>
          <span>Przewidywalność harmonogramu</span>
          <span>Partnerskie podejście</span>
          <span>Skalowalność zespołu</span>
        </div>
      </section>

      <section>
        <h2>Model współpracy inwestor – DEMOCO – ja</h2>
        <div className="grid">
          {collaborationSteps.map((step) => (
            <article key={step.title} className="card">
              <h3>{step.title}</h3>
              <p>{step.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="cta">
        <h2>Efekt: mniej tarć, więcej wyniku</h2>
        <p>
          Jeśli szukasz współpracy, w której inwestor ma kontrolę, a generalny wykonawca
          ma przestrzeń do skutecznego dowiezienia kontraktu — zbudujmy to razem.
        </p>
        <a href="mailto:lukasz@hildebrandtmanagement.com">Umów rozmowę: lukasz@hildebrandtmanagement.com</a>
      </section>
    </main>
  )
}
