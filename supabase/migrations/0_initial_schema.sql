create extension if not exists "postgis" with schema "public" version '3.3.7';

create type "public"."estado_actividad" as enum ('pendiente', 'hecha');

create type "public"."rol_usuario" as enum ('administrador', 'supervisor', 'obrero');

create type "public"."severidad_enfermedad" as enum ('leve', 'moderada', 'alta');

create type "public"."tipo_ubicacion" as enum ('invernadero', 'lote');

create table "public"."actividades_planificadas" (
    "id" uuid not null default gen_random_uuid(),
    "fecha_programada" date not null,
    "descripcion" text not null,
    "tipo_labor_id" uuid,
    "perfil_id" uuid,
    "estado" estado_actividad default 'pendiente'::estado_actividad,
    "origen" text,
    "created_at" timestamp without time zone default now()
);


create table "public"."catalogo_enfermedades" (
    "id" uuid not null default gen_random_uuid(),
    "nombre" text not null,
    "descripcion" text,
    "tratamiento" text
);


create table "public"."detalle_insumos_aplicados" (
    "id" uuid not null default gen_random_uuid(),
    "aplicacion_id" uuid,
    "insumo_id" uuid,
    "cantidad" numeric,
    "unidad_id" uuid,
    "precio_unitario_usado" double precision,
    "costo_total" double precision
);


create table "public"."enfermedades_detectadas" (
    "id" uuid not null default gen_random_uuid(),
    "fecha" date not null,
    "ubicacion_id" uuid,
    "enfermedad_id" uuid,
    "severidad" severidad_enfermedad,
    "observaciones" text,
    "created_at" timestamp without time zone default now(),
    "created_by" uuid
);


create table "public"."fotos_enfermedad" (
    "id" uuid not null default gen_random_uuid(),
    "enfermedad_id" uuid,
    "url_foto" text
);


create table "public"."insumos" (
    "id" uuid not null default gen_random_uuid(),
    "nombre" text not null,
    "unidad_id" uuid,
    "precio_unitario" numeric,
    "tipo" text
);


create table "public"."insumos_aplicados" (
    "id" uuid not null default gen_random_uuid(),
    "fecha" date not null,
    "ubicacion_id" uuid,
    "observaciones" jsonb,
    "created_at" timestamp without time zone default now(),
    "created_by" uuid
);


create table "public"."labores" (
    "id" uuid not null default gen_random_uuid(),
    "fecha" date not null,
    "tipo_labor_id" uuid,
    "ubicacion_id" uuid,
    "perfil_id" uuid,
    "observaciones" text,
    "created_at" timestamp without time zone default now()
);


alter table "public"."labores" enable row level security;

create table "public"."perfiles" (
    "id" uuid not null default gen_random_uuid(),
    "user_id" uuid not null,
    "nombre" text not null,
    "rol" rol_usuario not null,
    "correo" text
);


create table "public"."precios_insumos" (
    "id" uuid not null default gen_random_uuid(),
    "insumo_id" uuid,
    "precio_unitario" double precision not null,
    "fecha_inicio" date not null,
    "fecha_fin" date,
    "created_at" timestamp with time zone default now()
);


create table "public"."produccion" (
    "id" uuid not null default gen_random_uuid(),
    "fecha" date not null,
    "ubicacion_id" uuid,
    "producto_id" uuid,
    "cantidad" numeric,
    "unidad_id" uuid,
    "observaciones" jsonb,
    "geolocalizacion" geometry(Point,4326),
    "created_at" timestamp without time zone default now(),
    "updated_at" timestamp without time zone default now(),
    "created_by" uuid,
    "latitud" double precision,
    "longitud" double precision
);


create table "public"."productos" (
    "id" uuid not null default gen_random_uuid(),
    "nombre" text not null,
    "unidad_id" uuid
);


alter table "public"."productos" enable row level security;

create table "public"."tipos_actividades" (
    "id" uuid not null default gen_random_uuid(),
    "nombre" text not null
);


alter table "public"."tipos_actividades" enable row level security;

create table "public"."tipos_labores" (
    "id" uuid not null default gen_random_uuid(),
    "nombre" text not null
);


alter table "public"."tipos_labores" enable row level security;

create table "public"."ubicaciones" (
    "id" uuid not null default gen_random_uuid(),
    "nombre" text not null,
    "tipo" tipo_ubicacion not null,
    "geolocalizacion" geometry(Point,4326),
    "descripcion" text
);


create table "public"."unidades" (
    "id" uuid not null default gen_random_uuid(),
    "nombre" text not null
);


alter table "public"."unidades" enable row level security;

CREATE UNIQUE INDEX actividades_planificadas_pkey ON public.actividades_planificadas USING btree (id);

CREATE UNIQUE INDEX catalogo_enfermedades_pkey ON public.catalogo_enfermedades USING btree (id);

CREATE UNIQUE INDEX detalle_insumos_aplicados_pkey ON public.detalle_insumos_aplicados USING btree (id);

CREATE UNIQUE INDEX enfermedades_detectadas_pkey ON public.enfermedades_detectadas USING btree (id);

CREATE UNIQUE INDEX fotos_enfermedad_pkey ON public.fotos_enfermedad USING btree (id);

CREATE UNIQUE INDEX insumos_aplicados_pkey ON public.insumos_aplicados USING btree (id);

CREATE UNIQUE INDEX insumos_pkey ON public.insumos USING btree (id);

CREATE UNIQUE INDEX labores_pkey ON public.labores USING btree (id);

CREATE UNIQUE INDEX perfiles_pkey ON public.perfiles USING btree (id);

CREATE UNIQUE INDEX perfiles_user_id_key ON public.perfiles USING btree (user_id);

CREATE INDEX precios_insumos_insumo_id_idx ON public.precios_insumos USING btree (insumo_id);

CREATE UNIQUE INDEX precios_insumos_pkey ON public.precios_insumos USING btree (id);

CREATE UNIQUE INDEX produccion_pkey ON public.produccion USING btree (id);

CREATE UNIQUE INDEX productos_pkey ON public.productos USING btree (id);

CREATE UNIQUE INDEX tipos_actividades_pkey ON public.tipos_actividades USING btree (id);

CREATE UNIQUE INDEX tipos_labores_pkey ON public.tipos_labores USING btree (id);

CREATE UNIQUE INDEX ubicaciones_pkey ON public.ubicaciones USING btree (id);

CREATE UNIQUE INDEX unidades_nombre_key ON public.unidades USING btree (nombre);

CREATE UNIQUE INDEX unidades_pkey ON public.unidades USING btree (id);

alter table "public"."actividades_planificadas" add constraint "actividades_planificadas_pkey" PRIMARY KEY using index "actividades_planificadas_pkey";

alter table "public"."catalogo_enfermedades" add constraint "catalogo_enfermedades_pkey" PRIMARY KEY using index "catalogo_enfermedades_pkey";

alter table "public"."detalle_insumos_aplicados" add constraint "detalle_insumos_aplicados_pkey" PRIMARY KEY using index "detalle_insumos_aplicados_pkey";

alter table "public"."enfermedades_detectadas" add constraint "enfermedades_detectadas_pkey" PRIMARY KEY using index "enfermedades_detectadas_pkey";

alter table "public"."fotos_enfermedad" add constraint "fotos_enfermedad_pkey" PRIMARY KEY using index "fotos_enfermedad_pkey";

alter table "public"."insumos" add constraint "insumos_pkey" PRIMARY KEY using index "insumos_pkey";

alter table "public"."insumos_aplicados" add constraint "insumos_aplicados_pkey" PRIMARY KEY using index "insumos_aplicados_pkey";

alter table "public"."labores" add constraint "labores_pkey" PRIMARY KEY using index "labores_pkey";

alter table "public"."perfiles" add constraint "perfiles_pkey" PRIMARY KEY using index "perfiles_pkey";

alter table "public"."precios_insumos" add constraint "precios_insumos_pkey" PRIMARY KEY using index "precios_insumos_pkey";

alter table "public"."produccion" add constraint "produccion_pkey" PRIMARY KEY using index "produccion_pkey";

alter table "public"."productos" add constraint "productos_pkey" PRIMARY KEY using index "productos_pkey";

alter table "public"."tipos_actividades" add constraint "tipos_actividades_pkey" PRIMARY KEY using index "tipos_actividades_pkey";

alter table "public"."tipos_labores" add constraint "tipos_labores_pkey" PRIMARY KEY using index "tipos_labores_pkey";

alter table "public"."ubicaciones" add constraint "ubicaciones_pkey" PRIMARY KEY using index "ubicaciones_pkey";

alter table "public"."unidades" add constraint "unidades_pkey" PRIMARY KEY using index "unidades_pkey";

alter table "public"."actividades_planificadas" add constraint "actividades_planificadas_perfil_id_fkey" FOREIGN KEY (perfil_id) REFERENCES perfiles(id) not valid;

alter table "public"."actividades_planificadas" validate constraint "actividades_planificadas_perfil_id_fkey";

alter table "public"."actividades_planificadas" add constraint "actividades_planificadas_tipo_labor_id_fkey" FOREIGN KEY (tipo_labor_id) REFERENCES tipos_labores(id) not valid;

alter table "public"."actividades_planificadas" validate constraint "actividades_planificadas_tipo_labor_id_fkey";

alter table "public"."detalle_insumos_aplicados" add constraint "detalle_insumos_aplicados_aplicacion_id_fkey" FOREIGN KEY (aplicacion_id) REFERENCES insumos_aplicados(id) ON DELETE CASCADE not valid;

alter table "public"."detalle_insumos_aplicados" validate constraint "detalle_insumos_aplicados_aplicacion_id_fkey";

alter table "public"."detalle_insumos_aplicados" add constraint "detalle_insumos_aplicados_insumo_id_fkey" FOREIGN KEY (insumo_id) REFERENCES insumos(id) not valid;

alter table "public"."detalle_insumos_aplicados" validate constraint "detalle_insumos_aplicados_insumo_id_fkey";

alter table "public"."detalle_insumos_aplicados" add constraint "detalle_insumos_aplicados_unidad_id_fkey" FOREIGN KEY (unidad_id) REFERENCES unidades(id) not valid;

alter table "public"."detalle_insumos_aplicados" validate constraint "detalle_insumos_aplicados_unidad_id_fkey";

alter table "public"."enfermedades_detectadas" add constraint "enfermedades_detectadas_created_by_fkey" FOREIGN KEY (created_by) REFERENCES perfiles(id) not valid;

alter table "public"."enfermedades_detectadas" validate constraint "enfermedades_detectadas_created_by_fkey";

alter table "public"."enfermedades_detectadas" add constraint "enfermedades_detectadas_enfermedad_id_fkey" FOREIGN KEY (enfermedad_id) REFERENCES catalogo_enfermedades(id) not valid;

alter table "public"."enfermedades_detectadas" validate constraint "enfermedades_detectadas_enfermedad_id_fkey";

alter table "public"."enfermedades_detectadas" add constraint "enfermedades_detectadas_ubicacion_id_fkey" FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id) not valid;

alter table "public"."enfermedades_detectadas" validate constraint "enfermedades_detectadas_ubicacion_id_fkey";

alter table "public"."fotos_enfermedad" add constraint "fotos_enfermedad_enfermedad_id_fkey" FOREIGN KEY (enfermedad_id) REFERENCES enfermedades_detectadas(id) ON DELETE CASCADE not valid;

alter table "public"."fotos_enfermedad" validate constraint "fotos_enfermedad_enfermedad_id_fkey";

alter table "public"."insumos" add constraint "insumos_unidad_id_fkey" FOREIGN KEY (unidad_id) REFERENCES unidades(id) not valid;

alter table "public"."insumos" validate constraint "insumos_unidad_id_fkey";

alter table "public"."insumos_aplicados" add constraint "insumos_aplicados_created_by_fkey" FOREIGN KEY (created_by) REFERENCES perfiles(id) not valid;

alter table "public"."insumos_aplicados" validate constraint "insumos_aplicados_created_by_fkey";

alter table "public"."insumos_aplicados" add constraint "insumos_aplicados_ubicacion_id_fkey" FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id) not valid;

alter table "public"."insumos_aplicados" validate constraint "insumos_aplicados_ubicacion_id_fkey";

alter table "public"."labores" add constraint "labores_perfil_id_fkey" FOREIGN KEY (perfil_id) REFERENCES perfiles(id) not valid;

alter table "public"."labores" validate constraint "labores_perfil_id_fkey";

alter table "public"."labores" add constraint "labores_tipo_labor_id_fkey" FOREIGN KEY (tipo_labor_id) REFERENCES tipos_labores(id) not valid;

alter table "public"."labores" validate constraint "labores_tipo_labor_id_fkey";

alter table "public"."labores" add constraint "labores_ubicacion_id_fkey" FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id) not valid;

alter table "public"."labores" validate constraint "labores_ubicacion_id_fkey";

alter table "public"."perfiles" add constraint "perfiles_user_id_key" UNIQUE using index "perfiles_user_id_key";

alter table "public"."precios_insumos" add constraint "precios_insumos_insumo_id_fkey" FOREIGN KEY (insumo_id) REFERENCES insumos(id) ON DELETE CASCADE not valid;

alter table "public"."precios_insumos" validate constraint "precios_insumos_insumo_id_fkey";

alter table "public"."produccion" add constraint "produccion_created_by_fkey" FOREIGN KEY (created_by) REFERENCES perfiles(id) not valid;

alter table "public"."produccion" validate constraint "produccion_created_by_fkey";

alter table "public"."produccion" add constraint "produccion_producto_id_fkey" FOREIGN KEY (producto_id) REFERENCES productos(id) not valid;

alter table "public"."produccion" validate constraint "produccion_producto_id_fkey";

alter table "public"."produccion" add constraint "produccion_ubicacion_id_fkey" FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id) not valid;

alter table "public"."produccion" validate constraint "produccion_ubicacion_id_fkey";

alter table "public"."produccion" add constraint "produccion_unidad_id_fkey" FOREIGN KEY (unidad_id) REFERENCES unidades(id) not valid;

alter table "public"."produccion" validate constraint "produccion_unidad_id_fkey";

alter table "public"."productos" add constraint "productos_unidad_id_fkey" FOREIGN KEY (unidad_id) REFERENCES unidades(id) not valid;

alter table "public"."productos" validate constraint "productos_unidad_id_fkey";

alter table "public"."unidades" add constraint "unidades_nombre_key" UNIQUE using index "unidades_nombre_key";

create type "public"."geometry_dump" as ("path" integer[], "geom" geometry);

create type "public"."valid_detail" as ("valid" boolean, "reason" character varying, "location" geometry);

create or replace view "public"."vista_insumos_aplicados_detallado" as  SELECT a.id AS aplicacion_id,
    a.fecha,
    a.ubicacion_id,
    a.observaciones,
    d.insumo_id,
    i.nombre AS insumo_nombre,
    d.cantidad,
    d.unidad_id,
    u.nombre AS unidad_nombre,
    d.precio_unitario_usado,
    ((d.cantidad)::double precision * d.precio_unitario_usado) AS costo_total_usd
   FROM (((insumos_aplicados a
     JOIN detalle_insumos_aplicados d ON ((a.id = d.aplicacion_id)))
     LEFT JOIN insumos i ON ((d.insumo_id = i.id)))
     LEFT JOIN unidades u ON ((d.unidad_id = u.id)));


grant delete on table "public"."actividades_planificadas" to "anon";

grant insert on table "public"."actividades_planificadas" to "anon";

grant references on table "public"."actividades_planificadas" to "anon";

grant select on table "public"."actividades_planificadas" to "anon";

grant trigger on table "public"."actividades_planificadas" to "anon";

grant truncate on table "public"."actividades_planificadas" to "anon";

grant update on table "public"."actividades_planificadas" to "anon";

grant delete on table "public"."actividades_planificadas" to "authenticated";

grant insert on table "public"."actividades_planificadas" to "authenticated";

grant references on table "public"."actividades_planificadas" to "authenticated";

grant select on table "public"."actividades_planificadas" to "authenticated";

grant trigger on table "public"."actividades_planificadas" to "authenticated";

grant truncate on table "public"."actividades_planificadas" to "authenticated";

grant update on table "public"."actividades_planificadas" to "authenticated";

grant delete on table "public"."actividades_planificadas" to "service_role";

grant insert on table "public"."actividades_planificadas" to "service_role";

grant references on table "public"."actividades_planificadas" to "service_role";

grant select on table "public"."actividades_planificadas" to "service_role";

grant trigger on table "public"."actividades_planificadas" to "service_role";

grant truncate on table "public"."actividades_planificadas" to "service_role";

grant update on table "public"."actividades_planificadas" to "service_role";

grant delete on table "public"."catalogo_enfermedades" to "anon";

grant insert on table "public"."catalogo_enfermedades" to "anon";

grant references on table "public"."catalogo_enfermedades" to "anon";

grant select on table "public"."catalogo_enfermedades" to "anon";

grant trigger on table "public"."catalogo_enfermedades" to "anon";

grant truncate on table "public"."catalogo_enfermedades" to "anon";

grant update on table "public"."catalogo_enfermedades" to "anon";

grant delete on table "public"."catalogo_enfermedades" to "authenticated";

grant insert on table "public"."catalogo_enfermedades" to "authenticated";

grant references on table "public"."catalogo_enfermedades" to "authenticated";

grant select on table "public"."catalogo_enfermedades" to "authenticated";

grant trigger on table "public"."catalogo_enfermedades" to "authenticated";

grant truncate on table "public"."catalogo_enfermedades" to "authenticated";

grant update on table "public"."catalogo_enfermedades" to "authenticated";

grant delete on table "public"."catalogo_enfermedades" to "service_role";

grant insert on table "public"."catalogo_enfermedades" to "service_role";

grant references on table "public"."catalogo_enfermedades" to "service_role";

grant select on table "public"."catalogo_enfermedades" to "service_role";

grant trigger on table "public"."catalogo_enfermedades" to "service_role";

grant truncate on table "public"."catalogo_enfermedades" to "service_role";

grant update on table "public"."catalogo_enfermedades" to "service_role";

grant delete on table "public"."detalle_insumos_aplicados" to "anon";

grant insert on table "public"."detalle_insumos_aplicados" to "anon";

grant references on table "public"."detalle_insumos_aplicados" to "anon";

grant select on table "public"."detalle_insumos_aplicados" to "anon";

grant trigger on table "public"."detalle_insumos_aplicados" to "anon";

grant truncate on table "public"."detalle_insumos_aplicados" to "anon";

grant update on table "public"."detalle_insumos_aplicados" to "anon";

grant delete on table "public"."detalle_insumos_aplicados" to "authenticated";

grant insert on table "public"."detalle_insumos_aplicados" to "authenticated";

grant references on table "public"."detalle_insumos_aplicados" to "authenticated";

grant select on table "public"."detalle_insumos_aplicados" to "authenticated";

grant trigger on table "public"."detalle_insumos_aplicados" to "authenticated";

grant truncate on table "public"."detalle_insumos_aplicados" to "authenticated";

grant update on table "public"."detalle_insumos_aplicados" to "authenticated";

grant delete on table "public"."detalle_insumos_aplicados" to "service_role";

grant insert on table "public"."detalle_insumos_aplicados" to "service_role";

grant references on table "public"."detalle_insumos_aplicados" to "service_role";

grant select on table "public"."detalle_insumos_aplicados" to "service_role";

grant trigger on table "public"."detalle_insumos_aplicados" to "service_role";

grant truncate on table "public"."detalle_insumos_aplicados" to "service_role";

grant update on table "public"."detalle_insumos_aplicados" to "service_role";

grant delete on table "public"."enfermedades_detectadas" to "anon";

grant insert on table "public"."enfermedades_detectadas" to "anon";

grant references on table "public"."enfermedades_detectadas" to "anon";

grant select on table "public"."enfermedades_detectadas" to "anon";

grant trigger on table "public"."enfermedades_detectadas" to "anon";

grant truncate on table "public"."enfermedades_detectadas" to "anon";

grant update on table "public"."enfermedades_detectadas" to "anon";

grant delete on table "public"."enfermedades_detectadas" to "authenticated";

grant insert on table "public"."enfermedades_detectadas" to "authenticated";

grant references on table "public"."enfermedades_detectadas" to "authenticated";

grant select on table "public"."enfermedades_detectadas" to "authenticated";

grant trigger on table "public"."enfermedades_detectadas" to "authenticated";

grant truncate on table "public"."enfermedades_detectadas" to "authenticated";

grant update on table "public"."enfermedades_detectadas" to "authenticated";

grant delete on table "public"."enfermedades_detectadas" to "service_role";

grant insert on table "public"."enfermedades_detectadas" to "service_role";

grant references on table "public"."enfermedades_detectadas" to "service_role";

grant select on table "public"."enfermedades_detectadas" to "service_role";

grant trigger on table "public"."enfermedades_detectadas" to "service_role";

grant truncate on table "public"."enfermedades_detectadas" to "service_role";

grant update on table "public"."enfermedades_detectadas" to "service_role";

grant delete on table "public"."fotos_enfermedad" to "anon";

grant insert on table "public"."fotos_enfermedad" to "anon";

grant references on table "public"."fotos_enfermedad" to "anon";

grant select on table "public"."fotos_enfermedad" to "anon";

grant trigger on table "public"."fotos_enfermedad" to "anon";

grant truncate on table "public"."fotos_enfermedad" to "anon";

grant update on table "public"."fotos_enfermedad" to "anon";

grant delete on table "public"."fotos_enfermedad" to "authenticated";

grant insert on table "public"."fotos_enfermedad" to "authenticated";

grant references on table "public"."fotos_enfermedad" to "authenticated";

grant select on table "public"."fotos_enfermedad" to "authenticated";

grant trigger on table "public"."fotos_enfermedad" to "authenticated";

grant truncate on table "public"."fotos_enfermedad" to "authenticated";

grant update on table "public"."fotos_enfermedad" to "authenticated";

grant delete on table "public"."fotos_enfermedad" to "service_role";

grant insert on table "public"."fotos_enfermedad" to "service_role";

grant references on table "public"."fotos_enfermedad" to "service_role";

grant select on table "public"."fotos_enfermedad" to "service_role";

grant trigger on table "public"."fotos_enfermedad" to "service_role";

grant truncate on table "public"."fotos_enfermedad" to "service_role";

grant update on table "public"."fotos_enfermedad" to "service_role";

grant delete on table "public"."insumos" to "anon";

grant insert on table "public"."insumos" to "anon";

grant references on table "public"."insumos" to "anon";

grant select on table "public"."insumos" to "anon";

grant trigger on table "public"."insumos" to "anon";

grant truncate on table "public"."insumos" to "anon";

grant update on table "public"."insumos" to "anon";

grant delete on table "public"."insumos" to "authenticated";

grant insert on table "public"."insumos" to "authenticated";

grant references on table "public"."insumos" to "authenticated";

grant select on table "public"."insumos" to "authenticated";

grant trigger on table "public"."insumos" to "authenticated";

grant truncate on table "public"."insumos" to "authenticated";

grant update on table "public"."insumos" to "authenticated";

grant delete on table "public"."insumos" to "service_role";

grant insert on table "public"."insumos" to "service_role";

grant references on table "public"."insumos" to "service_role";

grant select on table "public"."insumos" to "service_role";

grant trigger on table "public"."insumos" to "service_role";

grant truncate on table "public"."insumos" to "service_role";

grant update on table "public"."insumos" to "service_role";

grant delete on table "public"."insumos_aplicados" to "anon";

grant insert on table "public"."insumos_aplicados" to "anon";

grant references on table "public"."insumos_aplicados" to "anon";

grant select on table "public"."insumos_aplicados" to "anon";

grant trigger on table "public"."insumos_aplicados" to "anon";

grant truncate on table "public"."insumos_aplicados" to "anon";

grant update on table "public"."insumos_aplicados" to "anon";

grant delete on table "public"."insumos_aplicados" to "authenticated";

grant insert on table "public"."insumos_aplicados" to "authenticated";

grant references on table "public"."insumos_aplicados" to "authenticated";

grant select on table "public"."insumos_aplicados" to "authenticated";

grant trigger on table "public"."insumos_aplicados" to "authenticated";

grant truncate on table "public"."insumos_aplicados" to "authenticated";

grant update on table "public"."insumos_aplicados" to "authenticated";

grant delete on table "public"."insumos_aplicados" to "service_role";

grant insert on table "public"."insumos_aplicados" to "service_role";

grant references on table "public"."insumos_aplicados" to "service_role";

grant select on table "public"."insumos_aplicados" to "service_role";

grant trigger on table "public"."insumos_aplicados" to "service_role";

grant truncate on table "public"."insumos_aplicados" to "service_role";

grant update on table "public"."insumos_aplicados" to "service_role";

grant delete on table "public"."labores" to "anon";

grant insert on table "public"."labores" to "anon";

grant references on table "public"."labores" to "anon";

grant select on table "public"."labores" to "anon";

grant trigger on table "public"."labores" to "anon";

grant truncate on table "public"."labores" to "anon";

grant update on table "public"."labores" to "anon";

grant delete on table "public"."labores" to "authenticated";

grant insert on table "public"."labores" to "authenticated";

grant references on table "public"."labores" to "authenticated";

grant select on table "public"."labores" to "authenticated";

grant trigger on table "public"."labores" to "authenticated";

grant truncate on table "public"."labores" to "authenticated";

grant update on table "public"."labores" to "authenticated";

grant delete on table "public"."labores" to "service_role";

grant insert on table "public"."labores" to "service_role";

grant references on table "public"."labores" to "service_role";

grant select on table "public"."labores" to "service_role";

grant trigger on table "public"."labores" to "service_role";

grant truncate on table "public"."labores" to "service_role";

grant update on table "public"."labores" to "service_role";

grant delete on table "public"."perfiles" to "anon";

grant insert on table "public"."perfiles" to "anon";

grant references on table "public"."perfiles" to "anon";

grant select on table "public"."perfiles" to "anon";

grant trigger on table "public"."perfiles" to "anon";

grant truncate on table "public"."perfiles" to "anon";

grant update on table "public"."perfiles" to "anon";

grant delete on table "public"."perfiles" to "authenticated";

grant insert on table "public"."perfiles" to "authenticated";

grant references on table "public"."perfiles" to "authenticated";

grant select on table "public"."perfiles" to "authenticated";

grant trigger on table "public"."perfiles" to "authenticated";

grant truncate on table "public"."perfiles" to "authenticated";

grant update on table "public"."perfiles" to "authenticated";

grant delete on table "public"."perfiles" to "service_role";

grant insert on table "public"."perfiles" to "service_role";

grant references on table "public"."perfiles" to "service_role";

grant select on table "public"."perfiles" to "service_role";

grant trigger on table "public"."perfiles" to "service_role";

grant truncate on table "public"."perfiles" to "service_role";

grant update on table "public"."perfiles" to "service_role";

grant delete on table "public"."precios_insumos" to "anon";

grant insert on table "public"."precios_insumos" to "anon";

grant references on table "public"."precios_insumos" to "anon";

grant select on table "public"."precios_insumos" to "anon";

grant trigger on table "public"."precios_insumos" to "anon";

grant truncate on table "public"."precios_insumos" to "anon";

grant update on table "public"."precios_insumos" to "anon";

grant delete on table "public"."precios_insumos" to "authenticated";

grant insert on table "public"."precios_insumos" to "authenticated";

grant references on table "public"."precios_insumos" to "authenticated";

grant select on table "public"."precios_insumos" to "authenticated";

grant trigger on table "public"."precios_insumos" to "authenticated";

grant truncate on table "public"."precios_insumos" to "authenticated";

grant update on table "public"."precios_insumos" to "authenticated";

grant delete on table "public"."precios_insumos" to "service_role";

grant insert on table "public"."precios_insumos" to "service_role";

grant references on table "public"."precios_insumos" to "service_role";

grant select on table "public"."precios_insumos" to "service_role";

grant trigger on table "public"."precios_insumos" to "service_role";

grant truncate on table "public"."precios_insumos" to "service_role";

grant update on table "public"."precios_insumos" to "service_role";

grant delete on table "public"."produccion" to "anon";

grant insert on table "public"."produccion" to "anon";

grant references on table "public"."produccion" to "anon";

grant select on table "public"."produccion" to "anon";

grant trigger on table "public"."produccion" to "anon";

grant truncate on table "public"."produccion" to "anon";

grant update on table "public"."produccion" to "anon";

grant delete on table "public"."produccion" to "authenticated";

grant insert on table "public"."produccion" to "authenticated";

grant references on table "public"."produccion" to "authenticated";

grant select on table "public"."produccion" to "authenticated";

grant trigger on table "public"."produccion" to "authenticated";

grant truncate on table "public"."produccion" to "authenticated";

grant update on table "public"."produccion" to "authenticated";

grant delete on table "public"."produccion" to "service_role";

grant insert on table "public"."produccion" to "service_role";

grant references on table "public"."produccion" to "service_role";

grant select on table "public"."produccion" to "service_role";

grant trigger on table "public"."produccion" to "service_role";

grant truncate on table "public"."produccion" to "service_role";

grant update on table "public"."produccion" to "service_role";

grant delete on table "public"."productos" to "anon";

grant insert on table "public"."productos" to "anon";

grant references on table "public"."productos" to "anon";

grant select on table "public"."productos" to "anon";

grant trigger on table "public"."productos" to "anon";

grant truncate on table "public"."productos" to "anon";

grant update on table "public"."productos" to "anon";

grant delete on table "public"."productos" to "authenticated";

grant insert on table "public"."productos" to "authenticated";

grant references on table "public"."productos" to "authenticated";

grant select on table "public"."productos" to "authenticated";

grant trigger on table "public"."productos" to "authenticated";

grant truncate on table "public"."productos" to "authenticated";

grant update on table "public"."productos" to "authenticated";

grant delete on table "public"."productos" to "service_role";

grant insert on table "public"."productos" to "service_role";

grant references on table "public"."productos" to "service_role";

grant select on table "public"."productos" to "service_role";

grant trigger on table "public"."productos" to "service_role";

grant truncate on table "public"."productos" to "service_role";

grant update on table "public"."productos" to "service_role";

grant delete on table "public"."spatial_ref_sys" to "anon";

grant insert on table "public"."spatial_ref_sys" to "anon";

grant references on table "public"."spatial_ref_sys" to "anon";

grant select on table "public"."spatial_ref_sys" to "anon";

grant trigger on table "public"."spatial_ref_sys" to "anon";

grant truncate on table "public"."spatial_ref_sys" to "anon";

grant update on table "public"."spatial_ref_sys" to "anon";

grant delete on table "public"."spatial_ref_sys" to "authenticated";

grant insert on table "public"."spatial_ref_sys" to "authenticated";

grant references on table "public"."spatial_ref_sys" to "authenticated";

grant select on table "public"."spatial_ref_sys" to "authenticated";

grant trigger on table "public"."spatial_ref_sys" to "authenticated";

grant truncate on table "public"."spatial_ref_sys" to "authenticated";

grant update on table "public"."spatial_ref_sys" to "authenticated";

grant delete on table "public"."spatial_ref_sys" to "postgres";

grant insert on table "public"."spatial_ref_sys" to "postgres";

grant references on table "public"."spatial_ref_sys" to "postgres";

grant select on table "public"."spatial_ref_sys" to "postgres";

grant trigger on table "public"."spatial_ref_sys" to "postgres";

grant truncate on table "public"."spatial_ref_sys" to "postgres";

grant update on table "public"."spatial_ref_sys" to "postgres";

grant delete on table "public"."spatial_ref_sys" to "service_role";

grant insert on table "public"."spatial_ref_sys" to "service_role";

grant references on table "public"."spatial_ref_sys" to "service_role";

grant select on table "public"."spatial_ref_sys" to "service_role";

grant trigger on table "public"."spatial_ref_sys" to "service_role";

grant truncate on table "public"."spatial_ref_sys" to "service_role";

grant update on table "public"."spatial_ref_sys" to "service_role";

grant delete on table "public"."tipos_actividades" to "anon";

grant insert on table "public"."tipos_actividades" to "anon";

grant references on table "public"."tipos_actividades" to "anon";

grant select on table "public"."tipos_actividades" to "anon";

grant trigger on table "public"."tipos_actividades" to "anon";

grant truncate on table "public"."tipos_actividades" to "anon";

grant update on table "public"."tipos_actividades" to "anon";

grant delete on table "public"."tipos_actividades" to "authenticated";

grant insert on table "public"."tipos_actividades" to "authenticated";

grant references on table "public"."tipos_actividades" to "authenticated";

grant select on table "public"."tipos_actividades" to "authenticated";

grant trigger on table "public"."tipos_actividades" to "authenticated";

grant truncate on table "public"."tipos_actividades" to "authenticated";

grant update on table "public"."tipos_actividades" to "authenticated";

grant delete on table "public"."tipos_actividades" to "service_role";

grant insert on table "public"."tipos_actividades" to "service_role";

grant references on table "public"."tipos_actividades" to "service_role";

grant select on table "public"."tipos_actividades" to "service_role";

grant trigger on table "public"."tipos_actividades" to "service_role";

grant truncate on table "public"."tipos_actividades" to "service_role";

grant update on table "public"."tipos_actividades" to "service_role";

grant delete on table "public"."tipos_labores" to "anon";

grant insert on table "public"."tipos_labores" to "anon";

grant references on table "public"."tipos_labores" to "anon";

grant select on table "public"."tipos_labores" to "anon";

grant trigger on table "public"."tipos_labores" to "anon";

grant truncate on table "public"."tipos_labores" to "anon";

grant update on table "public"."tipos_labores" to "anon";

grant delete on table "public"."tipos_labores" to "authenticated";

grant insert on table "public"."tipos_labores" to "authenticated";

grant references on table "public"."tipos_labores" to "authenticated";

grant select on table "public"."tipos_labores" to "authenticated";

grant trigger on table "public"."tipos_labores" to "authenticated";

grant truncate on table "public"."tipos_labores" to "authenticated";

grant update on table "public"."tipos_labores" to "authenticated";

grant delete on table "public"."tipos_labores" to "service_role";

grant insert on table "public"."tipos_labores" to "service_role";

grant references on table "public"."tipos_labores" to "service_role";

grant select on table "public"."tipos_labores" to "service_role";

grant trigger on table "public"."tipos_labores" to "service_role";

grant truncate on table "public"."tipos_labores" to "service_role";

grant update on table "public"."tipos_labores" to "service_role";

grant delete on table "public"."ubicaciones" to "anon";

grant insert on table "public"."ubicaciones" to "anon";

grant references on table "public"."ubicaciones" to "anon";

grant select on table "public"."ubicaciones" to "anon";

grant trigger on table "public"."ubicaciones" to "anon";

grant truncate on table "public"."ubicaciones" to "anon";

grant update on table "public"."ubicaciones" to "anon";

grant delete on table "public"."ubicaciones" to "authenticated";

grant insert on table "public"."ubicaciones" to "authenticated";

grant references on table "public"."ubicaciones" to "authenticated";

grant select on table "public"."ubicaciones" to "authenticated";

grant trigger on table "public"."ubicaciones" to "authenticated";

grant truncate on table "public"."ubicaciones" to "authenticated";

grant update on table "public"."ubicaciones" to "authenticated";

grant delete on table "public"."ubicaciones" to "service_role";

grant insert on table "public"."ubicaciones" to "service_role";

grant references on table "public"."ubicaciones" to "service_role";

grant select on table "public"."ubicaciones" to "service_role";

grant trigger on table "public"."ubicaciones" to "service_role";

grant truncate on table "public"."ubicaciones" to "service_role";

grant update on table "public"."ubicaciones" to "service_role";

grant delete on table "public"."unidades" to "anon";

grant insert on table "public"."unidades" to "anon";

grant references on table "public"."unidades" to "anon";

grant select on table "public"."unidades" to "anon";

grant trigger on table "public"."unidades" to "anon";

grant truncate on table "public"."unidades" to "anon";

grant update on table "public"."unidades" to "anon";

grant delete on table "public"."unidades" to "authenticated";

grant insert on table "public"."unidades" to "authenticated";

grant references on table "public"."unidades" to "authenticated";

grant select on table "public"."unidades" to "authenticated";

grant trigger on table "public"."unidades" to "authenticated";

grant truncate on table "public"."unidades" to "authenticated";

grant update on table "public"."unidades" to "authenticated";

grant delete on table "public"."unidades" to "service_role";

grant insert on table "public"."unidades" to "service_role";

grant references on table "public"."unidades" to "service_role";

grant select on table "public"."unidades" to "service_role";

grant trigger on table "public"."unidades" to "service_role";

grant truncate on table "public"."unidades" to "service_role";

grant update on table "public"."unidades" to "service_role";

create policy "Acceso a mis actividades"
on "public"."actividades_planificadas"
as permissive
for select
to public
using ((perfil_id IN ( SELECT perfiles.id
   FROM perfiles
  WHERE (perfiles.user_id = auth.uid()))));


create policy "insert"
on "public"."catalogo_enfermedades"
as permissive
for insert
to public
with check (true);


create policy "select"
on "public"."catalogo_enfermedades"
as permissive
for select
to public
using (true);


create policy "update"
on "public"."catalogo_enfermedades"
as permissive
for update
to public
using (true);


create policy "Libre acceso a insumos aplicados"
on "public"."detalle_insumos_aplicados"
as permissive
for all
to public
using (true);


create policy "Insert y select si soy autor"
on "public"."enfermedades_detectadas"
as permissive
for all
to public
using ((created_by = auth.uid()))
with check ((created_by = auth.uid()));


create policy "Acceso libre a fotos"
on "public"."fotos_enfermedad"
as permissive
for all
to public
using (true);


create policy "insert"
on "public"."insumos"
as permissive
for insert
to public
with check (true);


create policy "select"
on "public"."insumos"
as permissive
for select
to public
using (true);


create policy "update"
on "public"."insumos"
as permissive
for update
to public
using (true);


create policy "Insert y select si soy autor"
on "public"."insumos_aplicados"
as permissive
for all
to public
using ((created_by = auth.uid()))
with check ((created_by = auth.uid()));


create policy "Insertar y ver labores"
on "public"."labores"
as permissive
for all
to public
using (true)
with check (true);


create policy "Permitir acceso solo a su perfil"
on "public"."perfiles"
as permissive
for select
to public
using ((user_id = auth.uid()));


create policy "permitir insert a todos"
on "public"."produccion"
as permissive
for insert
to public
with check (true);


create policy "insert"
on "public"."productos"
as permissive
for insert
to public
with check (true);


create policy "select"
on "public"."productos"
as permissive
for select
to public
using (true);


create policy "update"
on "public"."productos"
as permissive
for update
to public
using (true);


create policy "insert"
on "public"."tipos_actividades"
as permissive
for insert
to public
with check (true);


create policy "select"
on "public"."tipos_actividades"
as permissive
for select
to public
using (true);


create policy "update"
on "public"."tipos_actividades"
as permissive
for update
to public
using (true);


create policy "Enable insert for authenticated users only"
on "public"."tipos_labores"
as permissive
for insert
to authenticated
with check (true);


create policy "Enable read access for all users"
on "public"."tipos_labores"
as permissive
for select
to public
using (true);


create policy "update"
on "public"."tipos_labores"
as permissive
for update
to public
using (true);


create policy "Enable insert for authenticated users only"
on "public"."ubicaciones"
as permissive
for insert
to authenticated
with check (true);


create policy "Enable read access for all users"
on "public"."ubicaciones"
as permissive
for select
to public
using (true);


create policy "update"
on "public"."ubicaciones"
as permissive
for update
to public
using (true);


create policy "Enable insert for authenticated users only"
on "public"."unidades"
as permissive
for insert
to authenticated
with check (true);


create policy "Enable read access for all users"
on "public"."unidades"
as permissive
for select
to public
using (true);




