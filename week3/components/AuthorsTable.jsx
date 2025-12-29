export default function AuthorsTable() {
  const authors = [
    {
      name: "Esthera Jackson",
      email: "esthera@simmple.com",
      avatar: "/Author/s1.svg",
      role: "Manager",
      department: "Organization",
      status: "Online",
      date: "14/06/21",
    },
    {
      name: "Alexa Liras",
      email: "alexa@simmple.com",
      avatar: "/Author/s2.svg",
      role: "Programmer",
      department: "Developer",
      status: "Offline",
      date: "14/06/21",
    },
    {
      name: "Laurent Michael",
      email: "laurent@simmple.com",
      avatar: "/Author/s3.svg",
      role: "Executive",
      department: "Projects",
      status: "Online",
      date: "14/06/21",
    },
    {
      name: "Frederardo Hill",
      email: "frederardo@simmple.com",
      avatar: "/Author/s4.svg",
      role: "Manager",
      department: "Organization",
      status: "Online",
      date: "14/06/21",
    },
    {
      name: "Daniel Thomas",
      email: "daniel@simmple.com",
      avatar: "/Author/s5.svg",
      role: "Programmer",
      department: "Developer",
      status: "Offline",
      date: "14/06/21",
    },
    {
      name: "Mark Wilson",
      email: "mark@simmple.com",
      avatar: "/Author/s6.svg",
      role: "Designer",
      department: "UI/UX Design",
      status: "Offline",
      date: "14/06/21",
    },
  ];

  return (
    <div className="bg-white rounded-2xl shadow-md pt-3 px-8 pb-1">
      <h3 className="font-bold text-xl text-gray-800 mb-6">Authors Table</h3>
      <div className="grid grid-cols-12 text-xs text-gray-400 font-semibold pb-3 border-b border-gray-200">
        <div className="col-span-4">AUTHOR</div>
        <div className="col-span-3">FUNCTION</div>
        <div className="col-span-2">STATUS</div>
        <div className="col-span-2">EMPLOYED</div>
        <div className="col-span-1"></div>
      </div>

      {/* Rows */}
      {authors.map((a, i) => (
        <div
          key={i}
          className="grid grid-cols-12 items-center py-4 border-b last:border-none"
        >
          <div className="col-span-4 flex items-center gap-3">
            <img
              src={a.avatar}
              className="w-10 h-10 rounded-full object-cover"
            />
            <div>
              <p className="text-sm font-bold text-gray-800">{a.name}</p>
              <p className="text-xs text-gray-500">{a.email}</p>
            </div>
          </div>

          <div className="col-span-3">
            <p className="text-sm font-bold text-gray-800">{a.role}</p>
            <p className="text-xs text-gray-500">{a.department}</p>
          </div>

          <div className="col-span-2">
            <span
              className={`px-3 py-1 text-xs rounded-full font-medium ${
                a.status === "Online"
                  ? "bg-green-500 font-bold text-xl rounded-2xl text-white text-green-600 px-4"
                  : "bg-gray-200 text-gray-500 px-4 rounded-2xl"
              }`}
            >
              {a.status}
            </span>
          </div>

          <div className="col-span-2 text-sm font-bold text-gray-700">
            {a.date}
          </div>

          <div className="col-span-1 text-sm text-gray-400 cursor-pointer">
            Edit
          </div>
        </div>
      ))}
    </div>
  );
}
