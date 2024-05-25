import { Generated, Insertable, Selectable, Updateable } from "kysely";

export interface MemberTable {
  id: Generated<number>;
  name: string;
  addressName: string;
  addressFullname: string;
  addressLongitude: string;
  addressLatitude: string;
}

export type Member = Selectable<MemberTable>;
export type NewMember = Insertable<MemberTable>;
export type MemberUpdate = Updateable<MemberTable>;
