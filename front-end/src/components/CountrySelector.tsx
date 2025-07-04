import Select from "react-select";

interface CountryOption {
  value: string;
  label: string;
}

interface Props {
  options: CountryOption[];
  selected: string[];
  onChange: (selected: string[]) => void;
}

export function CountrySelector({ options, selected, onChange }: Props) {
  const handleChange = (
    selectedOptions: readonly CountryOption[] | null
  ) => {
    onChange(selectedOptions ? Array.from(selectedOptions).map((opt) => opt.value) : []);
  };

  return (
    <div className="mb-4">
      <Select
        isMulti
        options={options}
        value={options.filter((opt) => selected.includes(opt.value))}
        onChange={handleChange}
        placeholder="Select countries..."
      />
    </div>
  );
}
