import AuthNavbar from "../components/ui/AuthNavbar";
import Footer from "../components/ui/Footer";
import Link from "next/link";

export default function SignIn() {
  return (
    <div className="min-h-screen bg-white relative overflow-hidden flex flex-col">
      {/* Navbar */}
      <AuthNavbar />
      <div className="flex flex-1 pt-28">
        <div className="w-[55%] flex items-center justify-center mt-20">
          <div className="w-[380px]">
            <h1 className="text-3xl font-bold text-teal-400 mb-2">
              Welcome Back
            </h1>

            <p className="text-sm text-gray-400 font-bold mb-8">
              Enter your email and password to sign in
            </p>

            <div className="space-y-5">
              <div>
                <label className="block text-sm text-gray-900 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  placeholder="Your email address"
                  className="w-full px-4 py-3 border border-gray-200 rounded-lg
                             text-sm text-gray-700 placeholder-gray-400
                             focus:outline-none focus:ring-2 focus:ring-teal-300"
                />
              </div>

              <div>
                <label className="block text-sm text-gray-900 mb-1">
                  Password
                </label>
                <input
                  type="password"
                  placeholder="Your password"
                  className="w-full px-4 py-3 border border-gray-200 rounded-lg
                             text-sm text-gray-700 placeholder-gray-400
                             focus:outline-none focus:ring-2 focus:ring-teal-300"
                />
              </div>

              <div className="flex items-center gap-2">
                <input type="checkbox" className="accent-teal-400" />
                <span className="text-sm text-gray-900">Remember me</span>
              </div>

              <button
                className="w-full bg-teal-400 text-white py-3 rounded-lg
                                 text-sm font-semibold hover:bg-teal-500 transition"
              >
                SIGN IN
              </button>

              <p className="text-sm text-gray-400 text-center">
                Don’t have an account?{" "}
                <Link href="/signup">
                <span className="text-teal-400 font-semibold cursor-pointer">
                  Sign up
                </span>
                </Link>
              </p>
            </div>
          </div>
        </div>
        <div className="w-[45%] h-[45vh] flex items-center justify-center pt-1 px-1">
          <div className="relative w-[100%] h-[100vh] rounded-[8px]">
            <img
              src="/chakra.svg"
              alt="Chakra Background"
              className=" absolute inset-0 w-full h-full object-cover rounded-l-[40px]"
            />
            <div
              className="relative z-10 flex items-center justify-center
                    h-full gap-4 -translate-y-[30px]"
            >
            </div>
          </div>
        </div>
      </div>
      <Footer/>
    </div>
  );
}
