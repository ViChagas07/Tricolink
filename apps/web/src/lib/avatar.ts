export const AVATAR_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"] as const;
export const MAX_AVATAR_FILE_BYTES = 5 * 1024 * 1024;
export const MAX_AVATAR_DATA_CHARS = 12_000;

export type PreparedAvatar = {
  content_type: "image/jpeg";
  data: string;
};

export type AvatarErrorCode = "type" | "size" | "processing";

export class AvatarError extends Error {
  readonly code: AvatarErrorCode;

  constructor(code: AvatarErrorCode) {
    super(`Avatar preparation failed: ${code}`);
    this.name = "AvatarError";
    this.code = code;
  }
}

export async function prepareAvatar(file: File): Promise<PreparedAvatar> {
  if (!AVATAR_MIME_TYPES.includes(file.type as (typeof AVATAR_MIME_TYPES)[number])) {
    throw new AvatarError("type");
  }
  if (file.size > MAX_AVATAR_FILE_BYTES) {
    throw new AvatarError("size");
  }

  let bitmap: ImageBitmap;
  try {
    bitmap = await createImageBitmap(file, { imageOrientation: "from-image" });
  } catch {
    throw new AvatarError("processing");
  }

  try {
    for (const size of [128, 96, 64]) {
      for (const quality of [0.82, 0.7, 0.58]) {
        const data = drawSquare(bitmap, size, quality);
        if (data.length <= MAX_AVATAR_DATA_CHARS) {
          return { content_type: "image/jpeg", data };
        }
      }
    }
  } finally {
    bitmap.close();
  }

  throw new AvatarError("size");
}

function drawSquare(bitmap: ImageBitmap, size: number, quality: number): string {
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const context = canvas.getContext("2d");
  if (!context) {
    throw new AvatarError("processing");
  }

  const side = Math.min(bitmap.width, bitmap.height);
  const sourceX = (bitmap.width - side) / 2;
  const sourceY = (bitmap.height - side) / 2;
  context.drawImage(bitmap, sourceX, sourceY, side, side, 0, 0, size, size);

  const dataUrl = canvas.toDataURL("image/jpeg", quality);
  return dataUrl.slice(dataUrl.indexOf(",") + 1);
}
