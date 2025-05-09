// frontend/app/layout.tsx
import "./globals.css";
import Link from "next/link";
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS

export const metadata = {
  title: "PaperWhiz – Your AI Research Assistant",
  description: "Upload, summarize, and ask questions about research papers.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 text-gray-900">
        <header className="bg-white shadow p-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">📄 PaperWhiz</h1>
          <nav className="space-x-4">
            <Link href="/">Home</Link>
            <Link href="/upload">Upload</Link>
            <Link href="/history">History</Link>
          </nav>
        </header>
        <main className="p-6 max-w-4xl mx-auto">{children}</main>
      </body>
    </html>
  );
}
