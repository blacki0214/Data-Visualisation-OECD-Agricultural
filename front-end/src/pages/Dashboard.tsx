import { useEffect, useState } from "react";
import { loadEnvData } from "../utils/loadData";
import type { EnvData } from "../types/EnvData";
import { TimeSeries } from "../components/TimeSeries";
import { CountrySelector } from "../components/CountrySelector";
import { filterProtectionCoefficient } from "../utils/filter"

export default function Dashboard() {
  const [data, setData] = useState<EnvData[]>([]);
  const [selectedCountries, setSelectedCountries] = useState<string[]>(["ARG"]);
  const [countryOptions, setCountryOptions] = useState<
    { value: string; label: string }[]
  >([]);

  useEffect(() => {
    loadEnvData().then((loadedData) => {
      async function fetchData() {
        const rawData = await loadEnvData();
        console.log("Raw data loaded:", rawData.length);

        // Cast or transform rawData to EnvData[] before filtering
        const typedRawData = rawData as unknown as EnvData[];
        const filteredData = filterProtectionCoefficient(typedRawData);
        console.log("Filtered protection data:", filteredData);

        setChartData(filteredData); // Assuming you have a state variable for chart data
      }

      fetchData();

      // Type cast the loaded data to EnvData[]
      const typedData = loadedData as unknown as EnvData[];
      setData(typedData);

      // Auto-generate unique country list
      const uniqueCountries = Array.from(
        new Set(typedData.map((d) => d.country_code))
      );

      setCountryOptions(
        uniqueCountries.map((code) => ({
          value: String(code),
          label: String(code),
        }))
      );
    });
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Agricultural Dashboard</h1>

      <CountrySelector
        options={countryOptions}
        selected={selectedCountries}
        onChange={setSelectedCountries}
      />

      <TimeSeries data={data} selectedCountries={selectedCountries} />
    </div>
  );
}
