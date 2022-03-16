function Field({ k, v }) {
  return (
    v && (
      <>
        <p>{k}</p>
        <p className={k}>{v}</p>
      </>
    )
  );
}

export default Field;
