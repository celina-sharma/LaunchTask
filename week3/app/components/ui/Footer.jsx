export default function Footer() {
  return (
    <footer className="border-t border-gray-100 mt-40">
      <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Left */}
        <p className="text-xs text-gray-400 text-center md:text-left">
          © 2021, Made with{" "}
          <span className="text-red-500">♥</span> by{" "}
          <span className="font-medium text-gray-500">Creative Tim</span> &{" "}
          <span className="font-medium text-gray-500">Simmmple</span>{" "}
          for a better web
        </p>

        {/* Right */}
        <div className="flex gap-10 text-xs text-gray-400">
          {["Creative Tim", "Simmmple", "Blog", "License"].map((item) => (
            <a
              key={item}
              href="#"
              className="hover:text-gray-900 transition"
            >
              {item}
            </a>
          ))}
        </div>
      </div>
    </footer>
  );
}
