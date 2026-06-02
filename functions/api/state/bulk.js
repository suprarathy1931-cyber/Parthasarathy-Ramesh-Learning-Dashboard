export async function onRequestPost(context) {

  const data = await context.request.json();

  await context.env.PROGRESS_KV.put(
    "state",
    JSON.stringify(data)
  );

  return Response.json({
    status:"ok"
  });
}
