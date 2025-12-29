export default function ProjectsTable() {
  const projects = [
    {
      name: "Chakra Soft UI Version",
      logo: "/Chakra UI.png",
      budget: "$14,000",
      status: "Working",
      progress: 60,
    },
    {
      name: "Add Progress Track",
      logo: "/Icon.png",
      budget: "$3,000",
      status: "Cancelled",
      progress: 10,
    },
    {
      name: "Fix Platform Errors",
      logo: "/Icon(1).png",
      budget: "Not set",
      status: "Done",
      progress: 100,
    },
    {
      name: "Launch our Mobile App",
      logo: "/Icon(2).png",
      budget: "$32,000",
      status: "Done",
      progress: 100,
    },
    {
      name: "Add the New Pricing Page",
      logo: "/Icon(3).png",
      budget: "$400",
      status: "Working",
      progress: 25,
    },
  ];

  return (
    <div className="bg-white rounded-2xl shadow-md pt-4 px-8 pb-5">
      <div className="mb-6">
        <h3 className="font-bold text-xl text-gray-800">Projects</h3>
        <p className="text-sm text-green-500">
          ✔ <span className="text-gray-400">30 done this month</span>
        </p>
      </div>
      <div className="grid grid-cols-12 text-xs text-gray-400 font-semibold pb-3 border-b border-gray-200">
        <div className="col-span-5">COMPANIES</div>
        <div className="col-span-2">BUDGET</div>
        <div className="col-span-2">STATUS</div>
        <div className="col-span-2">COMPLETION</div>
        <div className="col-span-1"></div>
      </div>

      {/* Rows */}
      {projects.map((project, idx) => (
        <div
          key={idx}
          className="grid grid-cols-12 items-center py-4 border-b last:border-none"
        >
          <div className="col-span-5 flex items-center gap-3">
            <img src={project.logo} alt="logo" className="w-8 h-8 rounded-lg" />
            <span className="text-sm font-bold text-gray-800">
              {project.name}
            </span>
          </div>

          <div className="col-span-2 text-sm font-semibold text-gray-700">
            {project.budget}
          </div>

          <div className="col-span-2 text-sm font-semibold text-gray-700">
            {project.status}
          </div>

          <div className="col-span-2 flex items-center gap-2">
            <span className="text-xs text-gray-600">{project.progress}%</span>
            <div className="w-full h-1.5 bg-gray-200 rounded-full">
              <div
                className="h-1.5 bg-teal-400 rounded-full"
                style={{ width: `${project.progress}%` }}
              />
            </div>
          </div>

          <div className="col-span-1 text-right text-gray-400 cursor-pointer">
            ⋮
          </div>
        </div>
      ))}
    </div>
  );
}
