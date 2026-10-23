import { describe, expect, it } from "vitest";

import { AvatarError, MAX_AVATAR_FILE_BYTES, prepareAvatar } from "./avatar";

describe("prepareAvatar", () => {
  it("rejects unsupported image types", async () => {
    const file = new File(["x"], "avatar.gif", { type: "image/gif" });

    await expect(prepareAvatar(file)).rejects.toMatchObject<Partial<AvatarError>>({
      code: "type",
    });
  });

  it("rejects files larger than 5 MB", async () => {
    const file = new File([new Uint8Array(MAX_AVATAR_FILE_BYTES + 1)], "avatar.png", {
      type: "image/png",
    });

    await expect(prepareAvatar(file)).rejects.toMatchObject<Partial<AvatarError>>({
      code: "size",
    });
  });
});
