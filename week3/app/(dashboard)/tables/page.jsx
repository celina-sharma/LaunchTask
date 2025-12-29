import AuthorsTable from "../../../components/AuthorsTable";
import ProjectsTable from "../../../components/ProjectsTable";
import Navbar from "@/app/components/ui/Navbar";
import Footer from "@/app/components/ui/Footer";

export default function TablesPage() {
  return (
    <div className="px-6 pt-2 pb-6 space-y-6">
      <Navbar/>
      <AuthorsTable />
      <ProjectsTable />
      <Footer/>
    </div>
  );
}
