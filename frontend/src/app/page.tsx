// frontend/app/page.tsx
import Link from "next/link";

export default function HomePage() {
  return (
    <section
      className="relative text-center mt-28 px-4 min-h-screen flex flex-col items-center justify-center
      bg-[url('/wp5121780.jpg')] bg-cover bg-center bg-no-repeat "
    >
      {/* Overlay for better text visibility */}
      <div className="absolute inset-0 bg-black/50"></div>

      {/* Content */}
      <div className="relative z-10">
        {/* Hero Heading */}
        <h2 className="text-5xl font-extrabold mb-6 text-white drop-shadow-[0_2px_6px_rgba(0,0,0,0.7)]">
          Welcome to PaperWhiz
        </h2>

        {/* Subheading */}
        <p className="mb-8 text-lg text-gray-100 max-w-2xl mx-auto">
          Your personal{" "}
          <span className="font-semibold">AI-powered assistant</span> for
          summarizing and understanding research papers. Upload, explore, and
          save time 🚀
        </p>

        {/* Call to Action */}
        <Link
          href="/upload"
          className="inline-block bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:opacity-90 text-white px-8 py-4 rounded-full font-semibold shadow-lg transition-transform transform hover:scale-105"
        >
          📄 Upload a Paper
        </Link>

        {/* Optional secondary action */}
        <div className="mt-6">
          <Link
            href="/history"
            className="inline-block px-6 py-3 rounded-full bg-gray-200/70 dark:bg-gray-800/70 text-gray-900 dark:text-gray-200 hover:bg-gray-300/80 dark:hover:bg-gray-700/80 transition"
          >
            View History
          </Link>
        </div>
      </div>
    </section>
  );
}
