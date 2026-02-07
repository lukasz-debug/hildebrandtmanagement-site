import './globals.css'

export const metadata = {
  title: 'Hildebrandt Management',
  description: 'Executive project leadership for construction & real estate',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pl">
      <body>{children}</body>
    </html>
  )
}
