const services = [
  {
    title: 'Strategia i rozwój firmy',
    description:
      'Pomagam właścicielom i zarządom poukładać cele, procesy oraz model działania tak, aby firma rosła szybciej i stabilniej.',
  },
  {
    title: 'Interim management',
    description:
      'Wchodzę do organizacji na czas transformacji, przejęcia projektu lub kryzysu operacyjnego i odpowiadam za dowiezienie wyniku.',
  },
  {
    title: 'Zarządzanie projektami budowlanymi',
    description:
      'Koordynuję inwestycje mieszkaniowe i komercyjne od etapu przygotowania po odbiory, dbając o budżet, harmonogram i jakość.',
  },
  {
    title: 'Optymalizacja i automatyzacje AI',
    description:
      'Wdrażam praktyczne usprawnienia pracy zespołów: standaryzację działań, automatyzację raportowania i narzędzia AI.',
  },
]

export default function Home() {
  return (
    <main>
      <section className="hero">
        <p className="eyebrow">Hildebrandt Management</p>
        <h1>Skuteczne zarządzanie dla firm, które chcą rosnąć szybciej</h1>
        <p className="lead">
          Wspieram właścicieli i zarządy firm z branży budowlanej oraz nieruchomości
          w porządkowaniu procesów, prowadzeniu projektów i realizacji ambitnych
          celów biznesowych.
        </p>
        <a className="btn" href="mailto:lukasz@hildebrandtmanagement.com">
          Umów konsultację
        </a>
      </section>

      <section>
        <h2>W czym mogę pomóc?</h2>
        <div className="grid">
          {services.map((service) => (
            <article key={service.title} className="card">
              <h3>{service.title}</h3>
              <p>{service.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="about">
        <h2>Dlaczego ja?</h2>
        <p>
          Od ponad 18 lat realizuję projekty o dużej skali i wysokiej złożoności.
          Łączę doświadczenie strategiczne z operacyjnym podejściem: diagnozuję,
          upraszczam i wdrażam rozwiązania, które dają mierzalny efekt.
        </p>
      </section>

      <section className="contact">
        <h2>Kontakt</h2>
        <p>
          Chcesz porozmawiać o współpracy? Napisz do mnie lub umów krótką,
          bezpłatną konsultację.
        </p>
        <a href="mailto:lukasz@hildebrandtmanagement.com">
          lukasz@hildebrandtmanagement.com
        </a>
      </section>
    </main>
  )
}
