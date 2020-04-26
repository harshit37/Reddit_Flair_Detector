import {Injectable} from '@angular/core'
import {HttpClient} from '@angular/common/http'
import {Observable} from 'rxjs'

@Injectable()
export class DetectorService{
    constructor(private http:HttpClient){}

    // addTask(task: Detector): Observable<Detector>{
    //     console.log(task);
    //     return this.http.post<Detector>('api/task',task);
    // }
}