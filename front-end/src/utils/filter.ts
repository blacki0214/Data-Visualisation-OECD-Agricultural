import type { EnvData } from "../types/EnvData";

export function filterProtectionCoefficient(data: EnvData[]) {
  console.log("Filter Protection - Input data length:", data.length);
  console.log("Available measures:", [...new Set(data.map(d => d.Measure))]);
  
  const filtered = data
    .filter((d) => {
      const matches = d.Measure === "Producer Nominal Protection Coefficient";
      return matches;
    })
    .map((d) => ({
      country: d.country_code,
      year: d.year,
      value: d.value,
    }));
  
  console.log("Filter Protection - Output data length:", filtered.length);
  return filtered;
}

export function getNutrientSurplusByCountry(
  data: EnvData[],
  nutrient: "Nitrogen" | "Phosphorus",
  year: number
) {
  return data.filter(
    (d) =>
      d.year === year &&
      d.nutrient_type === nutrient &&
      d.Measure.toLowerCase().includes("surplus")
  );
}

export function getScatterData(data: EnvData[], year: number) {
  const nitrogenInput = data.filter(
    (d) =>
      d.nutrient_type === "Nitrogen" &&
      d.Measure.toLowerCase().includes("input") &&
      d.year === year
  );

  const livestock = data.filter(
    (d) => d.Measure.toLowerCase().includes("livestock") && d.year === year
  );

  // You could merge/join them by country here
  const map = new Map<string, { nitrogen: number; livestock: number }>();

  nitrogenInput.forEach((row) => {
    map.set(row.country_code, {
      nitrogen: row.value,
      livestock: 0,
    });
  });

  livestock.forEach((row) => {
    const entry = map.get(row.country_code);
    if (entry) {
      entry.livestock += row.value;
    }
  });

  return Array.from(map.entries()).map(([country, values]) => ({
    country,
    ...values,
  }));
}

export function groupByMeasure(
  data: EnvData[],
  nutrient: string,
  year: number
) {
  return data.filter(
    (d) =>
      d.nutrient_type === nutrient &&
      d.year === year &&
      d.Measure.toLowerCase().includes("surplus")
  );
}
