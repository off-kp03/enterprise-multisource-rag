type Props = {
  title: string;
  subtitle: string;
  buttonText: string;
  onClick: () => void;
};

export default function SidePanel({
  title,
  subtitle,
  buttonText,
  onClick,
}: Props) {
  return (
    <div className="text-center space-y-6">
      <h2 className="text-3xl font-semibold tracking-tight">
        {title}
      </h2>

      <p className="text-neutral-400 text-sm leading-relaxed">
        {subtitle}
      </p>

      <button
        onClick={onClick}
        className="
          px-7 py-2.5
          text-sm font-medium
          rounded-md
          border border-neutral-300/40
          hover:bg-white hover:text-neutral-900
          transition
        "
      >
        {buttonText}
      </button>
    </div>
  );
}
