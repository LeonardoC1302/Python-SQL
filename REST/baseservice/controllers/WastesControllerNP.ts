import { Logger } from '../common'
import { data_wastesNoPool } from '../repositories/data_wastesNoPool'


export class WastesControllerNP {
    private static instance: WastesControllerNP;
    private log: Logger;

    private constructor()
    {
        this.log = new Logger();
        try
        {
        } catch (e)
        {
            this.log.error(e);
        }
    }

    public static getInstance() : WastesControllerNP
    {
        if (!this.instance)
        {
            this.instance = new WastesControllerNP();
        }
        return this.instance;
    }

    public getFilteredWastes(filter: number) : Promise<any> 
    {
        const wastesdata = new data_wastesNoPool();
        return wastesdata.getWasteMovementByQuantityNoPool(filter);
    }
}