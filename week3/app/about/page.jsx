import Link from "next/link";

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">

      {/* HERO */}
      <section className="bg-white py-20">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h1 className="text-4xl font-bold text-gray-800">
            About Purity UI Dashboard
          </h1>
          <p className="mt-4 text-gray-500 max-w-2xl mx-auto">
            A modern admin dashboard built with Next.js, Tailwind CSS,
            and real-world UI practices.
          </p>
        </div>
      </section>

      {/* CONTENT */}
      <section className="max-w-6xl mx-auto px-6 py-16 grid md:grid-cols-2 gap-12">
        <div>
          <h2 className="text-2xl font-semibold text-gray-800">
            Why this project?
          </h2>
          <p className="mt-4 text-gray-600 leading-relaxed">
            This dashboard was built to understand real production layouts,
            routing using the App Router, reusable components, and scalable
            UI architecture.
          </p>
          <p className="mt-4 text-gray-600">
            It includes analytics, tables, authentication pages,
            and a clean sidebar navigation.
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow p-8">
          <h3 className="font-semibold text-gray-800">
            Features Included
          </h3>
          <ul className="mt-4 space-y-2 text-gray-600">
            <li>✔ Dashboard Analytics</li>
            <li>✔ Projects & Orders</li>
            <li>✔ Authentication Pages</li>
            <li>✔ Sidebar & Navbar</li>
            <li>✔ Responsive Layout</li>
          </ul>
        </div>
      </section>
      <div className="text-center pb-20">
        <Link
          href="/dashboard"
          className="inline-block bg-teal-500 text-white px-6 py-3 rounded-xl font-semibold hover:bg-teal-600 transition"
        >
          Go to Dashboard →
        </Link>
      </div>

    </div>
  );
}
