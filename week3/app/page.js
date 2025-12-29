import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <section className="bg-gradient-to-br from-teal-400 to-teal-600 text-white py-32">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h1 className="text-4xl md:text-5xl font-bold">
            Build powerful dashboards faster
          </h1>

          <p className="mt-6 text-lg max-w-xl mx-auto text-teal-50 font-bold opacity-90">
            A powerful dashboard designed for clarity, speed, and control.
          </p>

          <div className="mt-10 flex justify-center gap-4">
            <Link
              href="/dashboard"
              className="bg-white text-teal-600 px-6 py-3 rounded-xl font-semibold shadow hover:scale-105 transition"
            >
              Dashboard
            </Link>

            <Link
              href="/about"
              className="border border-white px-8 py-3 rounded-xl font-semibold hover:bg-white hover:text-teal-600 transition"
            >
              About
            </Link>
          </div>
        </div>
      </section>
      <section className="max-w-6xl mx-auto px-6 py-20 grid md:grid-cols-3 gap-8">
        {[
          {
            title: "Clean UI",
            desc: "Minimal and professional layout inspired by Purity UI",
          },
          {
            title: "Scalable",
            desc: "Well-structured folders using App Router",
          },
          {
            title: "Production Ready",
            desc: "Reusable components & real-world patterns",
          },
        ].map((item, i) => (
          <div
            key={i}
            className="bg-white rounded-2xl p-6 shadow text-center"
          >
            <h3 className="font-semibold text-gray-800">{item.title}</h3>
            <p className="mt-2 text-gray-500 text-sm">{item.desc}</p>
          </div>
        ))}
      </section>
      <footer className="border-t border-gray-200 py-6 text-center text-sm text-gray-500">
        © 2025 • Purity UI Dashboard
      </footer>
    </div>
  );
}
