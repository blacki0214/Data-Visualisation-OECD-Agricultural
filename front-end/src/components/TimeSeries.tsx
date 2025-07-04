import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { EnvData } from "../types/EnvData";

interface TimeSeriesProps {
  data: EnvData[];
  selectedCountries: string[];
}

export function TimeSeries({ data, selectedCountries }: TimeSeriesProps) {
  // Filter only Producer Nominal Protection Coefficient
  const filtered = data.filter(
    (d) =>
      d.Measure === "Producer Nominal Protection Coefficient" &&
      selectedCountries.includes(d.country_code)
  );

  // Group by country
  const grouped: { [year: number]: any } = {};
  filtered.forEach((d) => {
    if (!grouped[d.year]) {
      grouped[d.year] = { year: d.year };
    }
    grouped[d.year][d.country_code] = d.value;
  });

  const chartData = Object.values(grouped).sort((a, b) => a.year - b.year);

  console.log("All data:", data);
  console.log("Filtered data:", filtered);
  console.log("Chart data:", chartData);

  return (
    <div className="p-4 bg-white shadow rounded-xl">
      <h2 className="text-xl font-semibold mb-4">Producer Nominal Protection Coefficient</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Legend />
          {selectedCountries.map((code) => (
            <Line
              key={code}
              type="monotone"
              dataKey={code}
              stroke={`#${Math.floor(Math.random() * 16777215).toString(16)}`}
              strokeWidth={2}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
