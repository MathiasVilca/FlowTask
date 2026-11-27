import { Service,inject } from '@angular/core';
import { HttpClient,HttpParams } from '@angular/common/http';
import { Observable,BehaviorSubject,tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { Task,TaskCreate,TaskUpdate } from '../models/task.model';
import { TaskStatus } from '../models/task.model';

@Service()
export class TaskService {
    private readonly http = inject(HttpClient);
    private readonly apiUrl = `${environment.apiUrl}/tasks`;
    private readonly tasksSubject = new BehaviorSubject<Task[]>([]);
    readonly tasks$ = this.tasksSubject.asObservable();
    
    loadTasks(status?: TaskStatus | '', categoryId?: number): Observable<Task[]>{
        let params = new HttpParams();
        if(status){
            params = params.set("status",status);
        }
        if(categoryId){
            params = params.set("category_id",categoryId)
        }
        return this.http.get<Task[]>(this.apiUrl,{params}).pipe(tap((tasks)=> this.tasksSubject.next(tasks)));
    }

    createTask(payload: TaskCreate): Observable<Task>{
        return this.http.post<Task>(this.apiUrl,payload);
    }

    updateTask(id: number, payload:TaskUpdate): Observable<Task>{
        return this.http.patch<Task>(`${this.apiUrl}/${id}`,payload);
    }

    deleteTask(id: number): Observable<{message:string,id:number}>{
        return this.http.delete<{message:string,id:number}>(`${this.apiUrl}/${id}`);
    }
}
