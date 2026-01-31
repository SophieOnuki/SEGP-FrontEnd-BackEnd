export interface Prediction {
  id: string;
  weight: number;
  volume?: number;
  timestamp: Date;
  imageUrl?: string;
}

