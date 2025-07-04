import * as d3 from "d3";

type EnvDataRecord = {
  Measure?: string;
  nutrient_type?: string;
  country_code?: string;
  [key: string]: any;
};

export async function loadEnvData() {
  try {
    console.log("Attempting to load data from: /data/cleaned_arg_env_data.csv");
    const data = await d3.csv<EnvDataRecord>("/data/cleaned_arg_env_data.csv", d3.autoType);
    console.log(`Loaded ${data.length} records`);
    
    if (data.length > 0) {
      console.log("First record:", data[0]);
      console.log("Available fields:", Object.keys(data[0]));
      console.log("Sample values:", {
        Measure: data.map(d => d.Measure).filter(Boolean).slice(0, 3),
        nutrient_type: data.map(d => d.nutrient_type).filter(Boolean).slice(0, 3),
        country_code: data.map(d => d.country_code).filter(Boolean).slice(0, 3)
      });
    } else {
      console.log("No data records were loaded");
    }
    
    return data;
  } catch (error) {
    console.error("Error loading data:", error);
    return [];
  }
}