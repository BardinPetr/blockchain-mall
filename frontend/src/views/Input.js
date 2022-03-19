function Input({ k, v, cb, ...props }) {
  return (
    <input className={k} onInput={cb} placeholder={k} {...props}>
      {v}
    </input>
  );
}

export default Input;
