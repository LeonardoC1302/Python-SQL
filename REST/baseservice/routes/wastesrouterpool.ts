import * as express from 'express';
import { Logger } from '../common'
import { WastesControllerPool } from '../controllers/'

const app = express();
const log = new Logger();

app.post("/getfilteredwastes", (req, res,next) => {
    WastesControllerPool.getInstance().getFilteredWastes(req.body.filter)
    .then((data:any)=>{
        res.json(data);
    })
    .catch((err:any)=>{
        log.error(err);
        return "{msg: \"error\"}";
    });

});

export { app as wastesrouterpool };