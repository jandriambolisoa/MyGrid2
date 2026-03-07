export function performance (score: number, potential: number): number{
  return Math.round(score * 2 / potential * 100);
}