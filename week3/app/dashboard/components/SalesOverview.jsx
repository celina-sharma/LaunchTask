import Card from '../../components/ui/Card';
 
export default function SalesOverview() {
  return (
    <Card>
      <h3 className="text-sm font-semibold mb-1">Sales Overview</h3>
      <p className="text-xs text-gray-400 mb-4">(+5) more in 2021</p>
 
      <div className="h-64 flex items-center justify-center text-gray-300">
        Chart will go here
      </div>
    </Card>
  );
}