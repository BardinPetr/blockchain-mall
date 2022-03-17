function Button({ k, ...props }) {
  return (
    <button type="submit" className={k} {...props}>
      {k}
    </button>
  );
}

export default Button;
