export function computeScore (
  userPrediction: number,
  appPrediction: number,
  gridSize: number,
  parameters: any
) {

  const rarity = Math.abs(userPrediction - appPrediction)

  // Initializing score.
  let finalScore = 0

  for (const param of Object.keys(parameters)) {

    const paramPoints = Math.max(...parameters[param]);

    if (param.includes("rarity")) {

      const rarityMargin = parseInt(param.replace("rarity", ""), 10);

      if (rarityMargin === rarity) {
        finalScore += paramPoints;
      }

      continue;
    }

    switch (param) {

      case "position":
        if (paramPoints !== undefined) {
          finalScore += paramPoints;
        }
        break;

      case "top10":
        if (userPrediction <= 10 && paramPoints !== undefined) {
          finalScore += paramPoints;
        }
        break;

      case "top5":
        if (userPrediction <= 5 && paramPoints !== undefined) {
          finalScore += paramPoints;
        }
        break;

      case "top3":
        if (userPrediction <= 3 && paramPoints !== undefined) {
          finalScore += paramPoints;
        }
        break;

      case "top1":
        if (userPrediction === 1 && paramPoints !== undefined) {
          finalScore += paramPoints;
        }
        break;

      case "last":
        if (userPrediction === gridSize && paramPoints !== undefined) {
          finalScore += paramPoints;
        }
        break;

      case "penultimate":
        if (userPrediction === gridSize - 1 && paramPoints !== undefined) {
          finalScore += paramPoints;
        }
        break;
    }
  }

  return finalScore

}