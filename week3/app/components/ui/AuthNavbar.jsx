import Link from "next/link";
export default function AuthNavbar({ variant = "auth" }) {
  return (
    <div
      className={`z-50 px-8 py-3 opacity-85
  ${
    variant === "auth"
      ? "fixed top-4 left-1/2 -translate-x-1/2 bg-white shadow-md rounded-xl w-[50%]"
      : "relative w-[80%] bg-transparent"
  }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <img src="/logo.png" alt="Logo" className="w-6 h-6" />
          <span className="font-semibold text-sm tracking-wide text-gray-800">
            PURITY UI DASHBOARD
          </span>
        </div>
        <nav className="flex items-center gap-8 text-xs font-semibold text-gray-700">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 hover:text-black transition"
          >
            <img src="/PurityNav/dashboard.svg" alt="" />
            <span>Dashboard</span>
          </Link>
          <Link
            href="/dashboard/profile"
            className="flex items-center gap-2 hover:text-black transition"
          >
            <img src="/PurityNav/profile.svg" alt="" />
            <span>Profile</span>
          </Link>
          <Link
            href="/signup"
            className=" flex items-center gap-2 hover:text-black transition"
          >
            <img src="/PurityNav/signup.svg" alt="" />
            <span>Sign Up</span>
          </Link>
          <Link
            href="/signin"
            className=" flex items-center gap-2 hover:text-black transition"
          >
            <img src="/PurityNav/signin.svg" alt="" />
            <span>Sign In</span>
          </Link>
        </nav>
        <button
          className="bg-gray-900 text-white
                     text-xs px-4 py-2 rounded-full"
        >
          Free Download
        </button>
      </div>
    </div>
  );
}
