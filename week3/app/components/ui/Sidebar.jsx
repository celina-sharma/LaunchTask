"use client";

import { usePathname, useRouter } from "next/navigation";
import {
  HomeIcon,
  TableCellsIcon,
  CreditCardIcon,
  WrenchScrewdriverIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
  UserPlusIcon,
  QuestionMarkCircleIcon,
} from "@heroicons/react/24/solid";

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-72 bg-white min-h-screen px-6 py-8 shadow-md">
      {/* Logo */}
      <div className="flex items-center gap-3 mb-12">
        <img
          src="/logo.png"
          alt="Purity UI Dashboard Logo"
          className="w-9 h-9"
        />
        <span className="font-semibold text-sm tracking-wide text-gray-800">
          PURITY UI DASHBOARD
        </span>
      </div>

      {/* Main menu */}
      <nav className="space-y-1">
        <SidebarItem
          icon={<HomeIcon />}
          label="Dashboard"
          route="/"
          active={pathname === "/"}
        />

        <SidebarItem
          icon={<TableCellsIcon />}
          label="Tables"
          route="/tables"
          active={pathname === "/tables"}
        />

        <SidebarItem
          icon={<CreditCardIcon />}
          label="Billing"
          route="/billing"
          active={pathname === "/billing"}
        />

        <SidebarItem
          icon={<WrenchScrewdriverIcon />}
          label="RTL"
          route="/rtl"
          active={pathname === "/rtl"}
        />
      </nav>

      {/* Account pages */}
      <p className="text-[11px] font-semibold text-gray-400 mt-10 mb-3 tracking-wider">
        ACCOUNT PAGES
      </p>

      <nav className="space-y-1">
        <SidebarItem icon={<UserIcon />} label="Profile" />
        <SidebarItem icon={<ArrowRightOnRectangleIcon />} label="Sign In" />
        <SidebarItem icon={<UserPlusIcon />} label="Sign Up" />
      </nav>

      {/* Help card */}
      <div className="mt-12 bg-gradient-to-br from-teal-400 to-teal-500 rounded-2xl p-5 text-white">
        <div className="bg-white/20 w-10 h-10 rounded-lg flex items-center justify-center mb-3">
          <QuestionMarkCircleIcon className="w-6 h-6" />
        </div>
        <p className="font-semibold text-sm">Need help?</p>
        <p className="text-xs opacity-90 mb-4">Please check our docs</p>
        <button className="w-full bg-white text-gray-800 text-xs font-semibold py-2 rounded-lg">
          DOCUMENTATION
        </button>
      </div>
    </aside>
  );
}

/* Sidebar Item */
function SidebarItem({ icon, label, route, active }) {
  const router = useRouter();

  return (
    <div
      onClick={() => route && router.push(route)}
      className={`flex items-center gap-4 px-4 py-3 rounded-xl text-sm cursor-pointer transition
        ${
          active
            ? "bg-gray-100 text-gray-900 font-semibold shadow-sm"
            : "text-gray-500 hover:bg-gray-100 hover:text-gray-800"
        }`}
    >
      <div
        className={`w-9 h-9 flex items-center justify-center rounded-lg
          ${active ? "bg-teal-400 text-white" : "bg-gray-100"}`}
      >
        <span className="w-5 h-5">{icon}</span>
      </div>
      {label}
    </div>
  );
}
