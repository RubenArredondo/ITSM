export type Rol = 'CLIENTE' | 'AGENTE' | 'SUPERVISOR';

export type Prioridad = 'BAJA' | 'MEDIA' | 'ALTA' | 'CRITICA';

export type Estado =
    | 'NUEVO'
    | 'EN_REVISION'
    | 'ESPERANDO_CLIENTE'
    | 'RESUELTO'
    | 'CERRADO';

export type Usuario = {
    id: number;
    username: string;
    rol: Rol;
    departamento_id: number | null;
    departamento_nombre: string | null;
};

export type Ticket = {
    id: number;
    titulo: string;
    descripcion: string;
    prioridad: Prioridad;
    estado: Estado;
    fecha_vencimiento_sla: string | null;
    fecha_creacion: string;
    fecha_actualizacion: string;
    solicitante: number;
    agente_asignado: number | null;
    departamento: number;
};

export type Comentario = {
    id: number;
    ticket: number;
    autor: number;
    autor_username: string;
    texto: string;
    fecha_creacion: string;
};
