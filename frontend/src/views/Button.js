function Button({ k, ...props }) {
  return (
    <button className={k} {...props}>
      {k}
    </button>
  );
}

export default Button;
