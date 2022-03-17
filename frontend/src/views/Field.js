function Field({ k, v, f }) {
  return (
    v ? (
      <>
        <p>>> {k}</p>
        <p className={k}>{f? f(v): v}</p>
      </>
    ) : null
  );
}

export default Field;
