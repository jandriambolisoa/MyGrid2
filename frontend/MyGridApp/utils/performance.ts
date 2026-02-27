export function performance (score: number, potential: number): number{
  return Math.round(score * 3 / potential * 100)
}