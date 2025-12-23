'use client';
 
import { usePathname } from 'next/navigation';
import {
  MagnifyingGlassIcon,
  UserIcon,
  CogIcon,
  BellIcon,
} from '@heroicons/react/24/outline';
 
export default function Navbar() {
  const pathname = usePathname();
 
  const slug = pathname === '/' ? 'dashboard' : pathname.replace('/', '');
 
  const pageName =
    slug.toLowerCase() === 'rtl'
      ? 'RTL'
      : slug.charAt(0).toUpperCase() + slug.slice(1);
 
  return (
    <header className="flex items-center justify-between px-6 py-4 bg-white">
      {/* Left */}
      <div>
        <p className="text-xs text-gray-400">Pages / {pageName}</p>
        <h1 className="text-lg font-semibold text-gray-800">{pageName}</h1>
      </div>
 
      {/* Right */}
      <div className="flex items-center gap-4">
        <div className="relative">
          <MagnifyingGlassIcon className="w-4 h-4 absolute left-3 top-2.5 text-gray-400" />
          <input
            type="text"
            placeholder="Type here..."
            className="pl-9 pr-4 py-2 text-sm rounded-full bg-gray-100 outline-none focus:ring-0"
          />
        </div>
 
        <div className="flex items-center gap-1 text-sm text-gray-600 cursor-pointer">
          <UserIcon className="w-4 h-4" />
          Sign In
        </div>
 
        <CogIcon className="w-5 h-5 text-gray-500 cursor-pointer" />
        <BellIcon className="w-5 h-5 text-gray-500 cursor-pointer" />
      </div>
    </header>
  );
}