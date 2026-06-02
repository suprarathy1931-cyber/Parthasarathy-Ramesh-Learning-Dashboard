export async function onRequestGet(context) {
  const state = await context.env.PROGRESS_KV.get("state");

  return Response.json(
    state ? JSON.parse(state) : {
      learnChecked:{},
      projectBuilt:{},
      phaseOpen:{},
      dsaTopics:{},
      dsaHeatmap:Array(182).fill(0),
      langPct:{},
      langSessions:{},
      schedule:{},
      notes:[],
      xp:0,
      streak:0,
      lastActive:""
    }
  );
}
