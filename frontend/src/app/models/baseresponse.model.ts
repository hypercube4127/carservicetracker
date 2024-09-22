export enum Level {
  INFO = "info",
  WARNING = "warning",
  ERROR = "error",
  SUCCESS = "success"
}

export type Message = {
  message: string;
  level: Level;
};

export type BaseResponse<T> = {
  data: T;
  messages: Message[];
  token: string;
};