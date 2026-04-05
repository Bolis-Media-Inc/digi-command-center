import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Digi Command Center',
  description: 'Real-time dashboard for Digi agent framework',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
