import {
  WalletIcon,
  GlobeAltIcon,
  DocumentTextIcon,
  ShoppingCartIcon,
} from "@heroicons/react/24/outline";

import {
  UserIcon,
  CursorArrowRaysIcon,
  ShoppingCartIcon as CartSolidIcon,
  CubeIcon,
} from "@heroicons/react/24/solid";

import StatCard from "../components/ui/StatCard";
import InfoCard from "../components/ui/InfoCard";
import ChakraBlock from "../components/ui/ChakraBlock";
import Footer from "../components/ui/Footer";


export default function Dashboard() {
  return (
    <div className="space-y-6">
      {/* ================= TOP 4 STAT CARDS ================= */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <StatCard
          title="Today's Money"
          value="$53,000"
          percentage="+55%"
          positive
          icon={<WalletIcon className="w-6 h-6" />}
        />
        <StatCard
          title="Today's Users"
          value="2,300"
          percentage="+5%"
          positive
          icon={<GlobeAltIcon className="w-6 h-6" />}
        />
        <StatCard
          title="New Clients"
          value="+3,052"
          percentage="-14%"
          positive={false}
          icon={<DocumentTextIcon className="w-6 h-6" />}
        />
        <StatCard
          title="Total Sales"
          value="$173,000"
          percentage="+8%"
          positive
          icon={<ShoppingCartIcon className="w-6 h-6" />}
        />
      </div>

      {/* ================= INFO + ROCKET CARD ================= */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2 bg-white rounded-2xl p-4 grid grid-cols-2 gap-6">
          <InfoCard />
          <ChakraBlock />
        </div>

        <div className="relative rounded-2xl overflow-hidden">
          <img
            src="/Background.png"
            alt="Work with the Rockets"
            className="absolute inset-0 w-full h-full"
          />
          <div className="relative z-10 p-7 flex flex-col h-full text-white">
            <h3 className="text-lg font-semibold">Work with the Rockets</h3>
            <p className="text-sm mt-2">
              Wealth creation is an evolutionarily recent positive-sum game. It
              is all about who take the opportunity first.
            </p>
            <span className="mt-auto text-sm">Read more →</span>
          </div>
        </div>
      </div>

      {/* ================= ANALYTICS ================= */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* ACTIVE USERS */}
        <div className="bg-white rounded-2xl p-1 xl:col-span-1">
          <div className="rounded-xl h-[180px] overflow-hidden">
            <img
              src="/Graph.svg"
              alt="Active Users Bar Chart"
              className="w-full h-full object-cover"
            />
          </div>

          <div className="mt-4">
            <h3 className="font-semibold">Active Users</h3>
            <p className="text-sm text-green-500">
              (+23) <span className="text-gray-400">than last week</span>
            </p>

            <div className="grid grid-cols-4 gap-4 mt-4">
              {[
                {
                  label: "Users",
                  value: "32,984",
                  icon: <UserIcon className="w-4 h-4 text-white" />,
                },
                {
                  label: "Clicks",
                  value: "2,42m",
                  icon: <CursorArrowRaysIcon className="w-4 h-4 text-white" />,
                },
                {
                  label: "Sales",
                  value: "$2,400",
                  icon: <CartSolidIcon className="w-4 h-4 text-white" />,
                },
                {
                  label: "Items",
                  value: "320",
                  icon: <CubeIcon className="w-4 h-4 text-white" />,
                },
              ].map((item) => (
                <div key={item.label} className="flex gap-3">
                  <div className="w-8 h-8 rounded-lg bg-teal-400 flex items-center justify-center">
                    {item.icon}
                  </div>
                  <div>
                    <p className="text-xs text-gray-400">{item.label}</p>
                    <p className="font-semibold text-sm">{item.value}</p>
                    <div className="h-[2px] w-10 bg-teal-400 mt-1 rounded-full" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* SALES OVERVIEW */}
        <div className="bg-white rounded-2xl p-6 xl:col-span-2">
          <h3 className="font-semibold">Sales overview</h3>
          <p className="text-sm text-green-500">
            (+5) <span className="text-gray-400">more in 2021</span>
          </p>
          <div className="mt-6 h-[260px]">
            <img
              src="/Graph(4).svg"
              alt="Sales Overview Chart"
              className="w-full h-full object-contain"
            />
          </div>
        </div>
      </div>
      {/* ================= PROJECTS & ORDERS ================= */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* ================= PROJECTS ================= */}
        <div className="xl:col-span-2 bg-white rounded-2xl p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800">Projects</h3>
              <p className="text-sm text-green-500">
                ✔ <span className="text-gray-400">30 done this month</span>
              </p>
            </div>
            <span className="text-gray-400 text-xl">⋮</span>
          </div>

          {/* Table Head */}
          <div className="grid grid-cols-4 text-xs text-gray-400 font-semibold pb-3 border-b border-gray-100">
            <span>COMPANIES</span>
            <span>MEMBERS</span>
            <span>BUDGET</span>
            <span>COMPLETION</span>
          </div>

          {/* ROW */}
          {[
            {
              name: "Chakra Soft UI Version",
              logo: "/Chakra UI.png",
              budget: "$14,000",
              progress: 60,
              members: ["/m1.png", "/m4.png"],
            },
            {
              name: "Add Progress Track",
              logo: "/Icon.png",
              budget: "$3,000",
              progress: 10,
              members: ["/m4.png"],
            },
            {
              name: "Fix Platform Errors",
              logo: "/Icon(1).png",
              budget: "Not set",
              progress: 100,
              members: ["/m5.png", "/m6.png"],
            },
            {
              name: "Launch our Mobile App",
              logo: "/Icon(2).png",
              budget: "$32,000",
              progress: 100,
              members: ["/m4.png"],
            },
            {
              name: "Add the New Pricing Page",
              logo: "/Icon(3).png",
              budget: "$400",
              progress: 25,
              members: ["/m5.png", "/m1.png"],
            },
            {
              name: "Redesign New Online Shop",
              logo: "/Icon(4).png",
              budget: "$7,600",
              progress: 40,
              members: ["/m6.png"],
            },
          ].map((item, idx) => (
            <div
              key={idx}
              className="grid grid-cols-4 items-center py-4 border-b border-gray-100 last:border-none"
            >
              {/* Company */}
              <div className="flex items-center gap-3">
                <img src={item.logo} className="w-6 h-6" />
                <span className="text-sm text-gray-800 font-medium">
                  {item.name}
                </span>
              </div>

              {/* Members */}
              <div className="flex -space-x-2">
                {item.members.map((m, i) => (
                  <img
                    key={i}
                    src={m}
                    className="w-8 h-8 rounded-full border-2 border-white object-cover bg-gray-300"
                  />
                ))}
              </div>

              {/* Budget */}
              <span className="text-sm text-gray-700">{item.budget}</span>
              <div>
                <span className="text-xs text-gray-500">{item.progress}%</span>
                <div className="w-full h-1 bg-gray-200 rounded-full mt-1">
                  <div
                    className="h-1 bg-teal-400 rounded-full"
                    style={{ width: `${item.progress}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* ================= ORDERS OVERVIEW ================= */}
        <div className="bg-white rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-gray-800">
            Orders overview
          </h3>
          <p className="text-sm text-green-500">
            +30% <span className="text-gray-400">this month</span>
          </p>

          <div className="space-y-5">
            {[
              {
                icon: "/Icon(5).png",
                title: "$2400, Design changes",
                time: "22 DEC 7:20 PM",
              },
              {
                icon: "/Icon(6).png",
                title: "New order #4219423",
                time: "21 DEC 11:21 PM",
              },
              {
                icon: "/Icon(7).png",
                title: "Server Payments for April",
                time: "21 DEC 9:28 PM",
              },
              {
                icon: "/Icon(8).png",
                title: "New card added for order #3210145",
                time: "20 DEC 3:52 PM",
              },
              {
                icon: "/Icon(9).png",
                title: "Unlock packages for Development",
                time: "19 DEC 11:35 PM",
              },
              {
                icon: "/Icon(10).png",
                title: "New order #9851258",
                time: "18 DEC 4:41 PM",
              },
            ].map((order, idx) => (
              <div key={idx} className="flex gap-4">
                {/* Timeline */}
                <div className="relative flex flex-col items-center">
                  {/* Vertical line */}
                  {idx !== order.length - 1 && (
                    <span className="absolute top-8 w-px h-full bg-gray-200" />
                  )}

                  {/* Icon */}
                  <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center z-10">
                    <img src={order.icon} className="w-5 h-5" />
                  </div>
                </div>

                {/* Content */}
                <div>
                  <p className="text-sm font-medium text-gray-800">
                    {order.title}
                  </p>
                  <p className="text-xs text-gray-400">{order.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      <Footer/>
    </div>
  );
}
