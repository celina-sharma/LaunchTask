import { BoltIcon } from "@heroicons/react/24/solid";

export default function ChakraBlock() {
  return (
    <div className="relative bg-teal-400 rounded-2xl w-full flex items-center justify-center overflow-hidden">
      {/* Decorative shapes */}
      <div className="absolute -top-16 -right-16 w-48 h-48 bg-white/10 rounded-full" />
      <div className="absolute -bottom-16 -left-16 w-48 h-48 bg-white/10 rounded-full" />

      {/* Content */}
      <div className="relative flex items-center gap-3">
        <div className="bg-white rounded-full p-3">
          <BoltIcon className="w-5 h-5 text-teal-400" />
        </div>
        <span className="text-white text-2xl font-bold">chakra</span>
      </div>
    </div>
  );
}
