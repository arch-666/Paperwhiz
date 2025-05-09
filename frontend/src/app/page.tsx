// frontend/app/page.tsx
import Link from "next/link";

export default function HomePage() {
  return (
    <section className="text-center mt-20">
      <h2 className="text-4xl font-semibold mb-4">Welcome to PaperWhiz</h2>
      <p className="mb-6 text-lg text-gray-600">
        Your personal AI-powered assistant for summarizing and understanding research papers.
      </p>
      <Link
        href="/upload"
        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition"
      >
        Upload a Paper
      </Link>
    </section>
  );
}
