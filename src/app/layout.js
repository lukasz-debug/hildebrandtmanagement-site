import './globals.css'

export const metadata = {
  title: 'Hildebrandt Management | Zarządzanie i rozwój firm',
  description:
    'Wsparcie zarządcze dla branży budowlanej i nieruchomości: strategia, interim management, projekty i optymalizacja procesów.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pl">
      <body>{children}</body>
    </html>
  )
}
