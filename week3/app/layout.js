import "./globals.css";
import Sidebar from "../components/ui/Sidebar";
import Navbar from "../components/ui/Navbar";
 
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <div className="flex min-h-screen">
          
          {/* Sidebar */}
          <Sidebar />
 
          {/* Right side */}
          <div className="flex flex-col flex-1">
            <Navbar />
            <main className="p-6">
              {children}
            </main>
          </div>
 
        </div>
      </body>
    </html>
  );
}