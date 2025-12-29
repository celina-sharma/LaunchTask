import Navbar from "@/app/components/ui/Navbar";
import { Toggle } from "@/app/components/ui/Toggle";
import Footer from "@/app/components/ui/Footer";
const conversations = [
  {
    name: "Esthera Jackson",
    message: "Hi! I need more informations...",
    avatar: "/avatar.svg",
  },
  {
    name: "Esthera Jackson",
    message: "Awesome work, can you change...",
    avatar: "/conversation/c1.svg",
  },
  {
    name: "Esthera Jackson",
    message: "Have a great afternoon...",
    avatar: "/conversation/c2.svg",
  },
  {
    name: "Esthera Jackson",
    message: "About files I can...",
    avatar: "/conversation/c3.svg",
  },
];
const projects = [
  {
    title: "Modern",
    description:
      "As Uber works through a huge amount of internal management turmoil.",
    image: "/Projects/p1.svg",
  },
  {
    title: "Scandinavian",
    description:
      "Music is something that every person has his or her own specific opinion about.",
    image: "/Projects/p2.svg",
  },
  {
    title: "Minimalist",
    description:
      "Different people have different taste, and various types of music.",
    image: "/Projects/p3.svg",
  },
];

export default function ProfilePage() {
  return (
    <div className="flex">
      {/* MAIN CONTENT */}
      <main className="flex-1 bg-gray-50 relative">
        <section className="relative h-[300px] overflow-hidden px-6 pt-6">
          <img
            src="/Background(2).svg"
            alt="Profile background"
            className="absolute inset-0 w-full h-full object-cover rounded-2xl"
          />

          {/* Navbar on top of background */}
          <div className="absolute top-0 left-0 w-full z-30 px-6">
            <Navbar variant="profile" />
          </div>
        </section>

        {/* ===== PROFILE SUMMARY CARD ===== */}
        <section className="relative ptx-6 -mt-20 z-20">
          <div className="bg-white rounded-xl shadow-md p-4 flex items-center justify-between">
            {/* Left */}
            <div className="flex items-center gap-4">
              <img
                src="/avatar.svg"
                alt="User"
                className="w-16 h-16 rounded-xl object-cover"
              />
              <div>
                <h2 className="font-semibold text-gray-900">Esthera Jackson</h2>
                <p className="text-sm text-gray-500">esthera@simmmple.com</p>
              </div>
            </div>

            {/* Right tabs */}
            <div className="flex gap-4 items-center">
              <img src="/Overview.svg" alt="Overview" />
              <img src="/Teams.svg" alt="Teams" />
              <img src="/Projects.svg" alt="Projects" />
            </div>
          </div>
        </section>

        {/* ===== INFO CARDS ===== */}
        <section className="px-6 mt-10 grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Platform Settings
            </h3>

            <p className="text-xs text-gray-400 mb-3">ACCOUNT</p>

            <div className="space-y-3 text-sm">
              <div className="flex items-center gap-3">
                <Toggle defaultChecked />
                <span className="text-gray-400">
                  Email me when someone follows me
                </span>
              </div>

              <div className="flex items-center gap-3">
                <Toggle />
                <span className="text-gray-400">
                  Email me when someone answers my post
                </span>
              </div>

              <div className="flex items-center gap-3">
                <Toggle defaultChecked />
                <span className="text-gray-400">
                  Email me when someone mentions me
                </span>
              </div>
            </div>

            <p className="text-xs text-gray-400 mt-6 mb-3">APPLICATION</p>

            <div className="space-y-3 text-sm">
              <div className="flex items-center gap-3">
                <Toggle />
                <span className="text-gray-400">New launches and projects</span>
              </div>

              <div className="flex items-center gap-3">
                <Toggle />
                <span className="text-gray-400">Monthly product updates</span>
              </div>

              <div className="flex items-center gap-3">
                <Toggle defaultChecked />
                <span className="text-gray-400">Subscribe to newsletter</span>
              </div>
            </div>
          </div>

          {/* PROFILE INFORMATION */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Profile Information
            </h3>

            <p className="text-sm text-gray-400 leading-relaxed mb-6">
              Hi, I'm Alec Thompson. Decisions: If you can't decide, the answer
              is no. If two equally difficult paths, choose the one more painful
              in the short term (pain avoidance is creating an illusion of
              equality).
            </p>

            <ul className="space-y-3 text-sm">
              <li>
                <span className="font-semibold text-gray-400">Full Name:</span>{" "}
                <span className="text-gray-500">Alec M. Thompson</span>
              </li>
              <li>
                <span className="font-semibold text-gray-400">Mobile:</span>{" "}
                <span className="text-gray-500">(44) 123 1234 123</span>
              </li>
              <li>
                <span className="font-semibold text-gray-400">Email:</span>{" "}
                <span className="text-gray-500">alec@simmmple.com</span>
              </li>
              <li>
                <span className="font-semibold text-gray-400">Location:</span>{" "}
                <span className="text-gray-500">United States</span>
              </li>

              <li className="flex items-center gap-3">
                <span className="font-semibold text-gray-400">Social:</span>
                <img src="/social.svg" className="w-10 h-7 cursor-pointer" />
              </li>
            </ul>
          </div>

          {/* CONVERSATIONS */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Conversations
            </h3>

            <div className="space-y-4">
              {conversations.map((item, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <img
                      src={item.avatar}
                      alt={item.name}
                      className="w-10 h-10 rounded-lg object-cover"
                    />
                    <div>
                      <p className="text-sm font-semibold text-gray-800">
                        {item.name}
                      </p>
                      <p className="text-xs text-gray-400 truncate w-[160px]">
                        {item.message}
                      </p>
                    </div>
                  </div>

                  <span className="text-xs font-semibold text-teal-400 cursor-pointer">
                    REPLY
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>
        {/* ===== PROJECTS SECTION ===== */}
        <section className="px-6 mt-10">
          <div className="bg-white rounded-2xl shadow-sm p-6">
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900">Projects</h3>
              <p className="text-sm text-gray-400">Architects design houses</p>
            </div>

            {/* Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
              {/* Project Cards */}
              {projects.map((project, i) => (
                <div
                  key={i}
                  className="bg-white rounded-xl shadow-md overflow-hidden"
                >
                  <img
                    src={project.image}
                    alt={project.title}
                    className="h-40 w-full object-cover"
                  />

                  {/* Content */}
                  <div className="p-4">
                    <p className="text-xs text-gray-400 mb-1">
                      Project #{i + 1}
                    </p>

                    <h4 className="font-semibold text-gray-900">
                      {project.title}
                    </h4>

                    <p className="text-xs text-gray-400 mt-2">
                      {project.description}
                    </p>
                    <div className="flex items-center justify-between mt-4">
                      <button className="text-xs px-4 py-2 border border-teal-400 text-teal-400 rounded-full hover:bg-teal-50 transition">
                        VIEW ALL
                      </button>

                      {/* Avatars */}
                      <div className="flex items-center -space-x-2">
                        <img
                          src="/m4.png"
                          className="w-6 h-6 rounded-full border-2 border-white object-cover"
                        />
                        <img
                          src="/m4.png"
                          className="w-6 h-6 rounded-full border-2 border-white object-cover"
                        />
                        <img
                          src="/m4.png"
                          className="w-6 h-6 rounded-full border-2 border-white object-cover"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-xl text-gray-400 hover:border-teal-400 hover:text-teal-400 transition cursor-pointer">
                <div className="text-3xl font-light mb-2">+</div>
                <p className="text-sm font-medium">Create a New Project</p>
              </div>
            </div>
          </div>
        </section>

        <Footer />
      </main>
    </div>
  );
}
