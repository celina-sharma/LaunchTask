'use client';

import { usePathname } from 'next/navigation';
import {
  MagnifyingGlassIcon,
  UserIcon,
  CogIcon,
  BellIcon,
} from '@heroicons/react/24/outline';

export default function Navbar({ variant = 'default' }) {
  const pathname = usePathname();

  const segments = pathname
    .split('/')
    .filter(Boolean)
    .filter(seg => seg !== 'dashboard');

  const page = segments.length === 0 ? 'dashboard' : segments.at(-1);
  const pageName =
    page.toLowerCase() === 'rtl'
      ? 'RTL'
      : page.charAt(0).toUpperCase() + page.slice(1);

  const isProfile = variant === 'profile';

  return (
    <header
      className={`w-full flex items-center justify-between px-6 py-4
      ${isProfile ? 'text-white' : 'bg-white text-gray-800'}`}
    >
      {/* LEFT */}
      <div>
        <p className={`text-xs ${isProfile ? 'text-white/70' : 'text-gray-400'}`}>
          Pages / {pageName}
        </p>
        <h1 className="text-lg font-semibold">{pageName}</h1>
      </div>

      {/* RIGHT */}
      <div className="flex items-center gap-4">
        <div className="relative">
          <MagnifyingGlassIcon
            className={`w-4 h-4 absolute left-3 top-2.5
            ${isProfile ? 'text-white' : 'text-gray-500'}`}
          />
          <input
            placeholder="Type here..."
            className={`pl-9 pr-4 py-2 text-sm rounded-full
              ${isProfile
                ? 'bg-white/20 text-white placeholder-white/70 caret-white'
                : 'bg-gray-100 text-gray-700 placeholder-gray-400'}
              focus:outline-none`}
          />
        </div>

        <div className="flex items-center gap-1 text-sm cursor-pointer">
          <UserIcon className="w-4 h-4" />
          Sign In
        </div>

        <CogIcon className="w-5 h-5 cursor-pointer" />
        <BellIcon className="w-5 h-5 cursor-pointer" />
      </div>
    </header>
  );
}
