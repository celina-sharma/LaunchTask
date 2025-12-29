import Sidebar from "../components/ui/Sidebar";
import Navbar from "../components/ui/Navbar";

export default function DashboardLayout({ children }) {
  return (
    <div className="flex min-h-screen bg-gray-50 ">
      <Sidebar />

      {/* Right side */}
      <div className="flex flex-col flex-1">
        {/* <Navbar /> */}
        <main className="px-1 pt-1 pb-2">
          {children}
        </main>
      </div>

    </div>
  );
}
